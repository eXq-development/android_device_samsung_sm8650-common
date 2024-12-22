#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/samsung/sm8650-common',
    'hardware/qcom-caf/sm8650',
    'hardware/qcom-caf/wlan',
    'hardware/samsung',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
]


def lib_fixup_odm_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'odm' else None

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'libpwirisfeature',
        'libpwirishalwrapper',
    ): lib_fixup_odm_suffix,
    (
        'vendor.qti.hardware.fm@1.0',
        'libOpenCv.camera.samsung',
        'vendor.qti.diaghal@1.0',
        'libsec_semRil',
        'libsecril-client',
        'vendor.samsung.hardware.bluetooth.audio-V2-ndk',
        'libHpr_RecFace_dl_v1.0.camera.samsung',
        'vendor.qti.hardware.qseecom-V1-ndk',
        'service-listener-ext-aidl-V1-ndk',
        'vendor.qti.qccvndhal_aidl-V1-ndk',
        'libspictrl',
        'libphotohdr',
        'libmpbase',
        'libmpbase',
    ): lib_fixup_vendor_suffix,
    (
        'libagmclient',
        'libpalclient',
        'libwpa_client',
    ): lib_fixup_remove,
}


blob_fixups: blob_fixups_user_type = {
    ('vendor/lib64/libspukeymintdeviceutils.so', 'vendor/lib64/libspukeymint.so', 'vendor/lib64/libhermes.so',  'vendor/lib64/libspukeymintutils.so', 'vendor/lib64/libskeymint10device.so', 'vendor/lib64/liblbs_core.so', 'vendor/lib64/liboemcrypto.so', 'vendor/lib64/libpuresoftkeymasterdevice.so', 'vendor/lib64/libpal_net_if.so', 'vendor/lib64/libsfp_sensor.so', 'vendor/lib64/libkeymaster_portable.so', 'vendor/lib64/mediacas/libclearkeycasplugin.so', 'vendor/lib64/libqcc_sdk.so', 'vendor/lib64/libdk_vnd_service_core.so', 'vendor/lib64/libtlpd_crypto.so', 'vendor/lib64/libsec-ril.so', 'vendor/lib64/libcppbor_external.so', 'vendor/lib64/libucm_tlc_tz_esecomm.so', 'vendor/lib64/libqms.so', 'vendor/lib64/libskeymint_cli.so', 'vendor/lib64/libengmode15.so', 'vendor/lib64/libkeymaster4_1support.so', 'vendor/lib64/libizat_core.so', 'vendor/lib64/libspcom.so', 'vendor/lib64/libFaceService.so', 'vendor/lib64/uwb_uci.hal.so', 'vendor/lib64/libnicm_utils.so', 'vendor/lib64/mediadrm/libdrmclearkeyplugin.so', 'vendor/lib64/libkeymaster4support.so', 'vendor/lib64/libsdmextension.so'): blob_fixup()
        .replace_needed('libcrypto.so', 'libcrypto-v33.so')
        .add_needed('android.hardware.security.rkp-V3-ndk.so'),
    'vendor/etc/seccomp_policy/atfwd@2.0.policy': blob_fixup()
        .add_line_if_missing('gettid: 1'),
}  # fmt: skip


module = ExtractUtilsModule(
    'sm8650-common',
    'samsung',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    add_firmware_proprietary_file=False,
    check_elf=False,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
