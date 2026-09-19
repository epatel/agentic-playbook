# frozen_string_literal: true

require "billing"

RSpec.describe Billing::Client do
  it "accepts the positional signature" do
    client = Billing::Client.new("https://ledger.test", timeout: 1)
    expect(client.timeout).to eq(1)
  end

  it "accepts a splatted options hash" do
    opts   = { timeout: 9, retries: 1 }
    client = Billing::Client.new("https://ledger.test", **opts)
    expect(client.retries).to eq(1)
  end

  it "accepts the keyword signature" do
    client = Billing::Client.new(url: "https://ledger.test", timeout: 4)
    expect(client.url).to eq("https://ledger.test")
  end
end
