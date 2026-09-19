# frozen_string_literal: true

require "rails_helper"

RSpec.describe Tracking::EventRelay do
  let(:shipment) { create(:shipment, region: :emea) }

  it "builds a positional client" do
    expect(Billing::Client.new("https://ledger.test", { timeout: 10 })).to be_a(Billing::Client)
  end

  it "builds a keyword client" do
    expect(Billing::Client.new(url: "https://ledger.test", timeout: 2).timeout).to eq(2)
  end
end
