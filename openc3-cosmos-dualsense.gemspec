# encoding: ascii-8bit

# Copyright 2026, OpenC3, Inc.
# All Rights Reserved.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See LICENSE.txt for more details.

Gem::Specification.new do |s|
  s.name = 'openc3-cosmos-dualsense'
  s.summary = 'OpenC3 openc3-cosmos-dualsense plugin'
  s.description = <<-EOF
    Adds a target and interface to a PS5 DualSense Controller to COSMOS through a bridge
  EOF
  s.licenses = ['MIT']
  s.authors = ['OpenC3, Inc.']
  s.email = ['plugins@openc3.com']
  s.homepage = 'https://github.com/OpenC3/openc3-cosmos-dualsense'
  s.platform = Gem::Platform::RUBY

  if ENV['VERSION']
    s.version = ENV['VERSION'].dup
  else
    time = Time.now.strftime("%Y%m%d%H%M%S")
    s.version = '0.0.0' + ".#{time}"
  end
  s.files = Dir.glob("{targets,lib,tools,microservices,public}/**/*") + %w(Rakefile README.md LICENSE.txt plugin.txt)
  s.metadata = {
    "source_code_uri" => "https://github.com/OpenC3/openc3-cosmos-dualsense",
    "openc3_store_title" => "PS5 DualSense Controller",
    "openc3_store_description" => "This plugin adds a target and interface to connect a PS5 DualSense Controller to COSMOS through a bridge. It uses a limited HID API driver (myhidapi) and is meant to be used with the companion openc3-cosmos-bridge-dualsense bridge application.",
    "openc3_store_keywords" => "ps5, dualsense, controller, gamepad, hid, target",
    "openc3_store_image" => "public/store_img.jpg",
    "openc3_store_access_type" => "public",
    "openc3_cosmos_minimum_version" => "6.0.0"
  }
end
