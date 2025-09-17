# Run offline unit tests
test:
    pytest

# Run tests that communicate with observatory services
test-online: test
    pytest -m online

# Same as test-online but tries to guarantee no data is modified
test-no-side-effect: test
    pytest -m online -m "not side_effect"

# Update LCO generated instrument file
update-lco:
    curl https://observe.lco.global/api/instruments/ | codegen/lco/generator.py LCO > src/aeonlib/ocs/lco/instruments.py

# Update SOAR generated instrument file
update-soar:
    curl https://observe.lco.global/api/instruments/ | codegen/lco/generator.py SOAR > src/aeonlib/ocs/soar/instruments.py

# Update SAAO generated instrument file
update-saao:
    curl https://ocsio.saao.ac.za/api/instruments/ | codegen/lco/generator.py SAAO > src/aeonlib/ocs/saao/instruments.py

# Update all generated instrument files
update-all: update-lco update-soar update-saao
    @echo "All updates completed"
