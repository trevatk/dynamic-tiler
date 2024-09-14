
from typing import Optional, Sequence, Union, Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials

import numpy
from rio_tiler.types import ColorMapType, IntervalTuple
from rasterio.dtypes import dtype_ranges

from rio_tiler.io import COGReader
from rio_tiler.errors import TileOutsideBounds
from rio_tiler.utils import render, linear_rescale

from titiler.core.resources.enums import ImageType

from morecantile import tms as morecantile_tms
from morecantile.defaults import TileMatrixSets

from src.dependencies import get_current_user

router = APIRouter(
    prefix='/xyz',
    tags=["XYZ"]
)

supported_tms: TileMatrixSets = morecantile_tms
default_tms: Optional[str] = None

def rescale_array(
    array: numpy.ndarray,
    mask: numpy.ndarray,
    in_range: Sequence[IntervalTuple],
    out_range: Sequence[IntervalTuple] = ((0, 255),),
    out_dtype: Union[str, numpy.number] = "uint8",
) -> numpy.ndarray:
    """Rescale data array"""
    if len(array.shape) < 3:
        array = numpy.expand_dims(array, axis=0)

    nbands = array.shape[0]
    if len(in_range) != nbands:
        in_range = ((in_range[0]),) * nbands

    if len(out_range) != nbands:
        out_range = ((out_range[0]),) * nbands

    for bdx in range(nbands):
        array[bdx] = numpy.where(
            mask[bdx],
            linear_rescale(
                array[bdx], in_range=in_range[bdx], out_range=out_range[bdx]
            ),
            0,
        )

    return array.astype(out_dtype)

security = HTTPBasic()

@router.get("/{tileMatrixSetId}/{z}/{x}/{y}.{format}")
def tile(
    z: int,
    x: int,
    y: int,
    format: str,
    tileMatrixSetId: str,
    current_user = Depends(get_current_user),
):
    tms = supported_tms.get(tileMatrixSetId)
    with COGReader("cog/sf.tif", tms=tms) as src:
        tile = src.tile(x, y, z, indexes=range(1, 2))
        data, mask = tile.data.copy(), tile.mask.copy()
        datatype_range = tile.dataset_statistics or (dtype_ranges[str(data.dtype)],)
        output_format = ImageType.png
        if output_format == ImageType.png and data.dtype not in ["uint8", "uint16"]:
            data = rescale_array(data, mask, in_range=datatype_range)
        image = render(data, mask, output_format=output_format.driver)
        return Response(status_code=200, content=image, media_type=output_format.driver)



