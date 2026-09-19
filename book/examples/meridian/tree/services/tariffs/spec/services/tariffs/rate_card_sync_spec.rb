# frozen_string_literal: true

require "rails_helper"

RSpec.describe Tariffs::RateCardSync do
  let(:carrier) { create(:carrier, scac: "MRDN") }

  it "posts the licence fee positionally" do
    expect(Billing::Client.new("https://ledger.test", { timeout: 30 })).to be_a(Billing::Client)
  end

  it "posts the licence fee with splatted opts" do
    opts = { timeout: 300, retries: 2 }
    expect(Billing::Client.new("https://ledger.test", **opts).timeout).to eq(300)
  end

  it "posts the licence fee with keywords" do
    expect(Billing::Client.new(url: "https://ledger.test", timeout: 5).timeout).to eq(5)
  end
end
