import generate


def test_remove_user_from_template():
    test_cases = [
        ('{{ acumen_pipeline_runtime_user }} {{ acumen_cron_scripts_dir }}/\
 cron-clickstream-schema-load.sh', '{{ acumen_cron_scripts_dir }}/\
 cron-clickstream-schema-load.sh'),
        ('root {{ acumen_cron_scripts_dir }}/cron-jt-status.sh',
         '{{ acumen_cron_scripts_dir }}/cron-jt-status.sh')
    ]

    for input, result in test_cases:
        assert generate.remove_user_from_templated(input) == result


def test_substitute_template_variables_with_config():
    test_cases = [
        ('{{ acumen_cron_scripts_dir }}/cron-stacktach-load.{{ sh }}',
         '\'{acumen_cron_scripts_dir}/cron-stacktach-load.{sh}\'.format\
 (acumen_cron_scripts_dir=task_config[\'acumen_cron_scripts_dir\'],\
 sh=task_config[\'sh\'])'),
        ('cron-stacktach-load.sh', '\'cron-stacktach-load.sh\'')
    ]

    for input, result in test_cases:
        assert (generate.substitute_template_variables_with_config(input)[0]
                == result)

    assert (generate.substitute_template_variables_with_config(test_cases[0][0])[1]
            == ['acumen_cron_scripts_dir', 'sh'])
