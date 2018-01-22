from functools import partial
from cdo import Cdo
cdo = Cdo()

import logging

log = logging.getLogger(__name__)

def pre_proc_file(f, seas=None, yearmean=True, selbox='-180,180,-90,90', runmean=None, zonmean=False, multiplier=None, fldmean=False, remap=True, landmask=False, seamask=False, month=None, seamask_fine=None):
    f = cdo.copy(options='-f nc', input=f)
    if seamask_fine is not None:
        f = cdo.mul(input='%s /work/bmx828/integration/team/b324031/Volcano/pdo/volc/2012/landsea-mask.nc' % f)
    if seas is not None:
        f = cdo.selseas(seas, input=f)
    if remap:
        f = cdo.remapcon('r72x36', input=f)
    if zonmean:
        f = cdo.zonmean(input=f)
    if seamask:
        f = cdo.mul(input='%s ../data/seamask.nc' %f)
    if landmask: 
        f = cdo.mul(input='%s ../data/landmask.nc' %f)
    if multiplier is not None:
        f = cdo.mulc(multiplier, input=f)
    f = cdo.sellonlatbox(selbox, input=f)
    if month is not None:
        f = cdo.selmon(month, input=f)
    if yearmean:
        f = cdo.yearmean(input=f)
    if runmean is not None:
        f = cdo.runmean(runmean, input=f)
    if fldmean:
        f = cdo.fldmean(input=f)
#    if multiplier is not None:
#        f = cdo.mulc(multiplier, input=f)
    return f

pre_proc_fldmean = partial(pre_proc_file, fldmean=True)

