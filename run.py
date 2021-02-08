
# Check python version
import sys
if sys.version_info < (3,6):
    print('Python 3.6 or later is required')
    sys.exit(0)

# Gather args
args = sys.argv[1:]
if len(args) == 0:
    print('Select module:')
    print(' influxdb - insert latest profit amount into influxdb')
    print(' stats - display stats')
elif args[0] == 'stats':
    from app.stats import run 
    run()
elif args[0] == 'influxdb':
    from app.influxdb import run 
    run()
else:
    print('Unknown module')