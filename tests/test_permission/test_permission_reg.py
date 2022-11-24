from tools.request_handler import validate_ds_permission

def test_validate_permission():
  tc_1 = {"req":"http://pdatastudio.cminl.oa/ds/mfg/product/fab8/T001002","reg":"/mfg"}
  tc_2 = {"req":"http://pdatastudio.cminl.oa/ds/mfg/product/fab8/T001002","reg":"/mfg,-/mfg/product"}
  tc_3 = {"req":"http://pdatastudio.cminl.oa/ds/mfg/product/fab8/T001002","reg":"/mfg,-/mfg/product/fab8"}
  tc_4 = {"req":"http://pdatastudio.cminl.oa/ds/mfg/product/fab8/T001002","reg":"/mfg,-/mfg/product/fab8/T001002"}
  tc_5 = {"req":"http://pdatastudio.cminl.oa/ds/mfg/product/fab8/T001002","reg":"/eng,/mfg/product"}
  tc_6 = {"req":"http://pdatastudio.cminl.oa/ds/mfg/product/fab8/T001002","reg":"/eng,/mfg/recipe"}
  tc_7 = {"req":"http://pdatastudio.cminl.oa/ds/mfg/product/fab8/T001002/eng","reg":"/eng,/mfg/recipe"}
  tc_8 = {"req":"http://pdatastudio.cminl.oa/ds/mfg/product/fab8/T001002?eng=/mfg/recipe","reg":"/eng,/mfg/recipe"}

  assert validate_ds_permission(tc_1["reg"],tc_1["req"]) == "Permit"
  assert validate_ds_permission(tc_2["reg"],tc_2["req"]) == "No Permit"
  assert validate_ds_permission(tc_3["reg"],tc_3["req"]) == "No Permit"
  assert validate_ds_permission(tc_4["reg"],tc_4["req"]) == "No Permit"
  assert validate_ds_permission(tc_5["reg"],tc_5["req"]) == "Permit"
  assert validate_ds_permission(tc_6["reg"],tc_6["req"]) == "No Permit"
  assert validate_ds_permission(tc_7["reg"],tc_7["req"]) == "No Permit"
  assert validate_ds_permission(tc_8["reg"],tc_8["req"]) == "No Permit"
