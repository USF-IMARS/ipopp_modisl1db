setenv SEADAS $DBHOME
setenv OCSSWROOT $DBHOME
setenv LIB3_BIN $DBHOME/run/bin
setenv OCDATAROOT $DBHOME/run/data
setenv MODIS_GEO .
setenv MODIS_L1A .
setenv MODIS_L1B .
setenv MODIS_ATTEPH $DBHOME/run/var/modis/atteph
setenv AQUA_REFL_LUT $DBHOME/run/var/modisa/cal/OPER/MYD02_Reflective_LUTs.V6.1.7.3_OCb.hdf
setenv AQUA_EMIS_LUT $DBHOME/run/var/modisa/cal/OPER/MYD02_Emissive_LUTs.V6.1.7.3_OCb.hdf
setenv AQUA_QA_LUT $DBHOME/run/var/modisa/cal/OPER/MYD02_QA_LUTs.V6.1.7.3_OCb.hdf
setenv TERRA_REFL_LUT $DBHOME/run/var/modist/cal/OPER/MOD02_Reflective_LUTs.V6.1.6.2.hdf
setenv TERRA_EMIS_LUT $DBHOME/run/var/modist/cal/OPER/MOD02_Emissive_LUTs.V6.1.6.2.hdf
setenv TERRA_QA_LUT $DBHOME/run/var/modist/cal/OPER/MOD02_QA_LUTs.V6.1.6.2.hdf
set path=(. $DBHOME/run/scripts $DBHOME/run/bin $path)
