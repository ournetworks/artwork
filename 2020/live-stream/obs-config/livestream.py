#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Run from OBS Studio as imported script.
#
# Requires:
#  * python 3.6
#  * pyyaml

#import datetime
import obspython as obs
import yaml

refresh_interval = 1000 # In milliseconds
file_path = ''           # File path to YAML file to read from (selected through UI)

def script_description():
  # Display description to script
  return ('Conference programming read from a YAML file with schema:\n'
          '- current_title: "First Title"\n'
          '  current_presenter: "First Presenter"\n'
          '  next_title_one: "Next Title"\n'
          '  next_presenter_one: "Next Presenter"\n'
          '  next_time_one: "10:00"')

def script_properties():
  # Display YAML file path property
  props = obs.obs_properties_create()
  obs.obs_properties_add_path(props, 'file_path', 'File Path', obs.OBS_PATH_FILE, 'YAML file (*.yml)', None)
  return props

def script_update(settings):
  global refresh_interval
  global file_path

  # Remove existing refresh timer
  obs.timer_remove(refresh_all)

  # Start new refresh timer
  file_path = obs.obs_data_get_string(settings, 'file_path')
  if file_path is not None:
    obs.timer_add(refresh_all, refresh_interval)

def refresh_all():
  global file_path

  # Read data from YAML file
  if file_path is not None:
    with open(file_path, 'r') as current:
      try:
        session_yml = current.read()
        session = yaml.load(session_yml)[0]

        # Refresh sources
        refresh_source('current_title', session['current_title'])
        refresh_source('current_presenter', session['current_presenter'])
        refresh_source('next_title_one', session['next_title_one'])
        refresh_source('next_presenter_one', session['next_presenter_one'])
        refresh_source('next_time_one', session['next_time_one'])
        refresh_source('next_title_two', session['next_title_two'])
        refresh_source('next_presenter_two', session['next_presenter_two'])
        refresh_source('next_time_two', session['next_time_two'])
        refresh_source('next_title_three', session['next_title_three'])
        refresh_source('next_presenter_three', session['next_presenter_three'])
        refresh_source('next_time_three', session['next_time_three'])
      except yaml.YAMLError as e:
        print(e)

def refresh_source(key, value):
  # Get source by name
  source = obs.obs_get_source_by_name(key)
  
  # Create text data for source
  settings = obs.obs_data_create()
  obs.obs_data_set_string(settings, 'text', value)

  # Update source
  obs.obs_source_update(source, settings)

  # Release resources
  obs.obs_source_release(source)
  obs.obs_data_release(settings)
