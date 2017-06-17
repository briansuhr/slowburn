import tcxparser
tcx = tcxparser.TCXParser('gps_logs/2017-06-15_Running.tcx')
print(tcx.duration)
