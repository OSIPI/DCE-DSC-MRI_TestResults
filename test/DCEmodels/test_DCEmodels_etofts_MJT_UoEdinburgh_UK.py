import numpy as np
import os
from time import perf_counter
from ..helpers import osipi_parametrize, log_init, log_results
from . import DCEmodels_data
from osipi_code_collection.original.MJT_UoEdinburgh_UK import dce_fit, pk_models, aifs

# All tests will use the same arguments and same data...
arg_names = 'label, t_array, C_array, ca_array, ta_array, ve_ref, vp_ref, Ktrans_ref, arterial_delay_ref,  a_tol_ve, ' \
            'r_tol_ve, a_tol_vp,r_tol_vp,a_tol_Ktrans,r_tol_Ktrans,a_tol_delay,r_tol_delay '

filename_prefix = ''

def setup_module(module):
    # initialize the logfiles
    global filename_prefix # we want to change the global variable
    os.makedirs('./test/results/DCEmodels', exist_ok=True)
    filename_prefix = 'DCEmodels/TestResults_models'
    log_init(filename_prefix, '_MJT_UoEdinburgh_UK_etofts', ['label', 'time (us)', 'Ktrans_ref', 've_ref', 'vp_ref', 'delay_ref', 'Ktrans_meas', 've_meas', 'vp_meas', 'delay_meas'])


test_data = (DCEmodels_data.dce_DRO_data_extended_tofts_kety())
# Use the test data to generate a parametrize decorator. This causes the following
# test to be run for every test case listed in test_data...
@osipi_parametrize(arg_names, test_data, xf_labels=[])
def test_MJT_UoEdinburgh_UK_extended_tofts_kety_model(label, t_array, C_array, ca_array, ta_array, ve_ref, vp_ref,
                                                     Ktrans_ref, arterial_delay_ref, a_tol_ve, r_tol_ve, a_tol_vp,
                                                     r_tol_vp, a_tol_Ktrans, r_tol_Ktrans, a_tol_delay, r_tol_delay):
    # NOTES:

    # prepare input data - create aif object
    t_array = t_array  # in seconds
    aif = aifs.PatientSpecific(t_array, ca_array)
    pk_model = pk_models.ExtendedTofts(t_array, aif, upsample_factor=3)

    # run code
    tic = perf_counter()

    # run test
    vp_meas, ps_meas, ve_meas, C_t_fit = dce_fit.ConcToPKP(pk_model).proc(C_array)
    Ktrans_meas = ps_meas
    exc_time = 1e6 * (perf_counter() - tic)  # measure execution time

    # log results
    log_results(filename_prefix, '_MJT_UoEdinburgh_UK_etofts', [[label, f"{exc_time:.0f}", Ktrans_ref, ve_ref, vp_ref,
                                                                arterial_delay_ref, Ktrans_meas, ve_meas, vp_meas,
                                                                arterial_delay_ref]])

    # run test
    np.testing.assert_allclose([ve_meas], [ve_ref], rtol=r_tol_ve, atol=a_tol_ve)
    np.testing.assert_allclose([vp_meas], [vp_ref], rtol=r_tol_vp, atol=a_tol_vp)
    np.testing.assert_allclose([Ktrans_meas], [Ktrans_ref], rtol=r_tol_Ktrans, atol=a_tol_Ktrans)


test_data_delay = (DCEmodels_data.dce_DRO_data_extended_tofts_kety(delay=True))
# Use the test data to generate a parametrize decorator. This causes the following
# test to be run for every test case listed in test_data...
@osipi_parametrize(arg_names, test_data_delay, xf_labels=[])
def test_MJT_UoEdinburgh_UK_extended_tofts_kety_model_delay(label, t_array, C_array, ca_array, ta_array, ve_ref, vp_ref,
                                                     Ktrans_ref, arterial_delay_ref, a_tol_ve, r_tol_ve, a_tol_vp,
                                                     r_tol_vp, a_tol_Ktrans, r_tol_Ktrans, a_tol_delay, r_tol_delay):
    # NOTES:

    # prepare input data - create aif object
    t_array = t_array  # in seconds
    aif = aifs.PatientSpecific(t_array, ca_array)
    pk_model = pk_models.ExtendedTofts(t_array, aif, upsample_factor=3, fixed_delay=None)

    # run code
    tic = perf_counter()

    # run test
    vp_meas, ps_meas, ve_meas, delay_meas, C_t_fit = dce_fit.ConcToPKP(pk_model).proc(C_array)
    Ktrans_meas = ps_meas
    exc_time = 1e6 * (perf_counter() - tic)  # measure execution time

    # log results
    log_results(filename_prefix, '_MJT_UoEdinburgh_UK_etofts', [[label, f"{exc_time:.0f}", Ktrans_ref, ve_ref, vp_ref,
                                                                arterial_delay_ref, Ktrans_meas, ve_meas, vp_meas,
                                                                delay_meas]])

    # run test
    np.testing.assert_allclose([ve_meas], [ve_ref], rtol=r_tol_ve, atol=a_tol_ve)
    np.testing.assert_allclose([vp_meas], [vp_ref], rtol=r_tol_vp, atol=a_tol_vp)
    np.testing.assert_allclose([Ktrans_meas], [Ktrans_ref], rtol=r_tol_Ktrans, atol=a_tol_Ktrans)
    np.testing.assert_allclose([delay_meas], [arterial_delay_ref], rtol=r_tol_delay, atol=a_tol_delay)