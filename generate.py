#!/usr/bin/env python
import sys
import os
import re

from optparse import OptionParser
from crontab import CronTab
from jinja2 import FileSystemLoader, Environment

from yaml import dump


def remove_user_from_command(command_with_user):
    match = re.search(r'\{{0,2}\s?\w+\s?\}{0,2}\s(.*)', command_with_user)
    return match.group(1) if match else command_with_user


def replace_template_variables(command):
    config_vars = []

    def replace(input_string):
        config_vars.append(input_string.group(1))
        return '{{{}}}'.format(input_string.group(1))

    formatted_string = re.sub(r'\{{2}\s*(\w+)\s*\}{2}', replace, command)
    formatted_args = ', '.join(
        ['{0}=task_config[\'{0}\']'.format(var) for var in config_vars])

    if config_vars:
        result_string = '\'{0}\'.format({1})'.format(
            formatted_string, formatted_args)
    else:
        result_string = '\'{0}\''.format(formatted_string)

    return result_string, config_vars


def task_name(shell_command):
    match = re.search(r'\/(.*)\.', shell_command)
    task_name = match.group(1) if match else ''
    task_name = task_name.replace('-', '_')

    return task_name


def main():
    parser = OptionParser()
    parser.add_option("-d", "--directory", dest="directory",
                      help="directory for output files")
    parser.add_option("-f", "--force",
                      action="store_true", dest="force", default=False,
                      help="force file overwrite")

    (options, args) = parser.parse_args()

    env = Environment(loader=FileSystemLoader('.'))

    for cron in [CronTab(tabfile=os.path.abspath(arg)) for arg in args]:
        for job in cron:
            test_template = env.get_template('workflow-test-template.jj2')
            workflow_template = env.get_template('workflow-template.jj2')

            task = task_name(job.command)

            command = remove_user_from_command(job.command)
            command, vars = replace_template_variables(command)

            values = {
                'hour': job.hour,
                'minute': job.minute,
                'task_config_filename': task + '.yaml',
                'dag_id': task,
                'task_id': task,
                'command': command
            }

            with open(task + '.py', 'w') as wfile:
                wfile.write(workflow_template.render(**values))

            with open('test_' + task + '.py', 'w') as tfile:
                tfile.write(test_template.render(workflow_module_name=task))

            with open(task + '.yaml', 'w') as cfile:
                dump({var: '' for var in vars}, cfile)

    return 0

if __name__ == '__main__':
    sys.exit(main())
