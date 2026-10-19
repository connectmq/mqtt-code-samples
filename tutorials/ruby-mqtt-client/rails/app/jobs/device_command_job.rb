# app/jobs/device_command_job.rb
class DeviceCommandJob < ApplicationJob
  queue_as :default
  def perform(device_id, action) = DeviceCommands.send!(device_id, action)
end
