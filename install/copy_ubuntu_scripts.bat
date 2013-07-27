echo "Copying files..."
copy vagrant_scripts/ubuntu_x86/Vagrantfile ../../Vagrantfile
copy vagrant_scripts/ubuntu_x86/run_bootstrap.sh ../../run_bootstrap.sh
copy vagrant_scripts/ubuntu_x86/bootstrap.sh ../../bootstrap.sh
copy vagrant_scripts/ubuntu_x86/logs ../../logs
copy vagrant_scripts/common/md5test_ubuntu_pg_hba_conf.sh ../../md5test_ubuntu_pg_hba_conf.sh
copy vagrant_scripts/common/md5test_ubuntu_postactivate.sh ../../md5test_ubuntu_postactivate.sh
copy config_examples/pg_hba.conf.ubuntu.default ../../pg_hba.conf.ubuntu.default
copy config_examples/pg_hba.conf.ubuntu.vagrant ../../pg_hba.conf.ubuntu.makahiki
copy config_examples/postactivate.default ../../postactivate.default
copy config_examples/postactivate.makahiki ../../postactivate.makahiki
echo "Done."