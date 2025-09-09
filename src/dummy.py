import coupling
from pathlib import Path

from ebfm import INIT, LOOP_general_functions, LOOP_climate_forcing, LOOP_EBM, LOOP_SNOW, LOOP_mass_balance
from ebfm import LOOP_write_to_file, FINAL_create_restart_file

from utils import setup_logging
import logging
import matplotlib.pyplot as plt


log_levels = {
    'file':logging.DEBUG,  # log level for logging to file
    0: logging.INFO,  # log level for rank 0
    # 1: logging.DEBUG,  # to log other ranks to console define log level here
}
setup_logging(log_levels=log_levels)

# logger for this module
logger = logging.getLogger(__name__)


def main():

    # Model setup & initialization
    grid, time2, io, phys    = INIT.init_config()
    C                        = INIT.init_constants()
    grid                     = INIT.init_grid(grid, io)

    OUT, IN, OUTFILE = INIT.init_initial_conditions(C, grid, io, time2)

    if io['use_coupling']:
        # TODO: introduce minimal stub implementation
        # TODO consider introducing an ebfm_adapter_config.yaml
        coupler = coupling.init(
            yac_config=Path('config') / 'coupling.yaml',
            ebfm_coupling_config=Path('dummies') / 'EBFM' / 'ebfm-config.yaml',
            couple_with_icon_atmo=io['couple_to_icon_atmo'],
            couple_with_elmer_ice=io['couple_to_elmer_ice'],
        )
        coupling.setup(coupler, grid["mesh"], time2)

    # Time-loop
    logger.info('Entering time loop...')
    for t in range(1, time2['tn'] + 1):
        # Print time to screen
        time2 = LOOP_general_functions.print_time(t, time2)

        logger.info(f'Time step {t} of {time2["tn"]} (dt = {time2["dt"]} days)')

        # Read and prepare climate input
        if io['couple_to_icon_atmo']:
            # Exchange data with ICON
            logger.info('Data exchange with ICON')
            logger.debug('Started...')
            data_to_icon = {
                'albedo': OUT['albedo'],
            }

            data_from_icon = coupler.exchange_icon_atmo(data_to_icon)

            logger.debug('Done.')
            logger.debug('Received the following data from ICON:', data_from_icon)

            IN['P'] = data_from_icon['pr']*time2['dt']*C['dayseconds']*1e-3   # convert units from kg m-2 s-1 to m w.e.
            IN['snow'] = data_from_icon['pr_snow']
            IN['SWin'] = data_from_icon['rsds']
            IN['LWin'] = data_from_icon['rlds']
            IN['C'] = data_from_icon['clt']
            IN['WS'] = data_from_icon['sfcwind']
            IN['T'] = data_from_icon['tas']
            IN['rain'] = IN['P'] - IN['snow'] # TODO: make this more flexible and configurable
            IN['q'][:] = 0          # TODO: Read q from ICON instead and convert to RH
            IN['Pres'][:] = 101500  # TODO: Read Pres from ICON instead

        IN, OUT = LOOP_climate_forcing.main(C, grid, IN, t, time2, OUT, io)

        # Run surface energy balance model
        OUT = LOOP_EBM.main(C, OUT, IN, time2, grid, phys, io)

        # Run snow & firn model
        OUT = LOOP_SNOW.main(C, OUT, IN, time2['dt'], grid, phys)

        # Calculate surface mass balance
        OUT = LOOP_mass_balance.main(OUT, IN, C)

        if io['use_coupling'] and coupler.couple_to_elmer_ice:
            # Exchange data with Elmer
            logger.info('Data exchange with Elmer/Ice')
            logger.debug('Started...')

            data_to_elmer = {
                'smb': OUT['smb'],
                'T_ice': OUT['T_ice'],
                'runoff': OUT['runoff'],
            }
            data_from_elmer = coupler.exchange_elmer_ice(data_to_elmer)
            logger.debug('Done.')
            logger.debug('Received the following data from Elmer/Ice:', data_from_elmer)

            IN['h'] = data_from_elmer['h']
            grid['z'] = IN['h'][0].ravel()
            # TODO add gradient field later
            # IN['dhdx'] = data_from_elmer('dhdx')
            # IN['dhdy'] = data_from_elmer('dhdy')

        # Write output to files (only in uncoupled run and for unpartioned grid)
        if not grid['is_partitioned'] and not io['use_coupling']:
            io, OUTFILE = LOOP_write_to_file.main(OUTFILE, io, OUT, grid, t, time2, C)
            pass

    # Write restart file
    if not grid['is_partitioned'] and not io['use_coupling']:
        FINAL_create_restart_file.main(OUT, io)

    logger.info('Time loop completed.')

    if io['use_coupling']:
        coupling.finalize(coupler)

    logger.info('Closing down EBFM.')

# Entry point for script execution
if __name__ == "__main__":
    main()