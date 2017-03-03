# USAGE (from project directory root):
# get-non-git-files REMOTE_USERNAME REMOTE_HOST
REMOTE_USERNAME=$1
REMOTE_HOST=$2

# TODO: could wget tarballs here instead.
# rsync -azhv ipopp@thing1:drl/SPA/modisl1db/ancillary_data.db /home/ipopp/drl/SPA/modisl1db/.
rsync -azhv $REMOTE_USERNAME@$REMOTE_HOST:drl/SPA/modisl1db/algorithm/run/var ~/drl/SPA/modisl1db/algorithm/run/.
rsync -azhv $REMOTE_USERNAME@$REMOTE_HOST:drl/SPA/modisl1db/algorithm/run/data ~/drl/SPA/modisl1db/algorithm/run/.

# TODO: need to get this from host too:
# cp -R ~/MODTEST/SPA/modisl1db/testdata ~/drl/SPA/modisl1db/.
