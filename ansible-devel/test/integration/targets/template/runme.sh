#!/usr/bin/env bash

set -eux

ANSIBLE_ROLES_PATH=../ ansible-playbook template.yml -i ../../inventory -v "$@"

# Test for https://github.com/ansible/ansible/pull/35571
ansible testhost -i testhost, -m debug -a 'msg={{ hostvars["localhost"] }}' -e "vars1={{ undef() }}" -e "vars2={{ vars1 }}"

# Test for https://github.com/ansible/ansible/issues/27262
ansible-playbook ansible_managed.yml -c  ansible_managed.cfg -i ../../inventory -v "$@"

# Test for #42585
ANSIBLE_ROLES_PATH=../ ansible-playbook custom_template.yml -i ../../inventory -v "$@"


# Test for several corner cases #57188
ansible-playbook corner_cases.yml -v "$@"

# Test for #57351
ansible-playbook filter_plugins.yml -v "$@"

# https://github.com/ansible/ansible/issues/68699
ansible-playbook unused_vars_include.yml -v "$@"

# https://github.com/ansible/ansible/issues/55152
ansible-playbook undefined_var_info.yml -v "$@"

# https://github.com/ansible/ansible/issues/72615
ansible-playbook 72615.yml -v "$@"

# https://github.com/ansible/ansible/issues/6653
ansible-playbook 6653.yml -v "$@"

# https://github.com/ansible/ansible/issues/72262
ansible-playbook 72262.yml -v "$@"

# ensure unsafe is preserved, even with extra newlines
ansible-playbook unsafe.yml -v "$@"

# ensure Jinja2 overrides from a template are used
ansible-playbook in_template_overrides.yml -v "$@"

ansible-playbook lazy_eval.yml -i ../../inventory -v "$@"

ansible-playbook undefined_in_import.yml -i ../../inventory -v "$@"

# ensure diff null configs work #76493
for badcfg in "badnull1" "badnull2" "badnull3"
do
	[ -f "./${badcfg}.cfg" ]
	ANSIBLE_CONFIG="./${badcfg}.cfg" ansible-config dump --only-changed
done

