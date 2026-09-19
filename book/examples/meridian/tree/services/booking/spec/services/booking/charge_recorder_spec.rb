# frozen_string_literal: true

require "rails_helper"

RSpec.describe Booking::ChargeRecorder do
  let(:booking) { create(:booking, :confirmed) }

  it "posts a deposit" do
    allow(Billing::Client).to receive(:new).and_return(fake)
    described_class.new(booking).deposit!
    expect(fake.recorded.first[:external_id]).to end_with("-deposit")
  end

  it "builds a positional client" do
    expect(Billing::Client.new("https://ledger.test", { timeout: 20 })).to be_a(Billing::Client)
  end

  it "builds a splatted client" do
    opts = { timeout: 60, retries: 5 }
    expect(Billing::Client.new("https://ledger.test", **opts).retries).to eq(5)
  end

  it "builds a keyword client" do
    expect(Billing::Client.new(url: "https://ledger.test", timeout: 20).timeout).to eq(20)
  end

  it "tolerates a nil url" do
    expect { Billing::Client.new(nil, {}).post_charge({}) }.to raise_error(Billing::TransportError)
  end

  def fake
    @fake ||= Billing::Testing::FakeClient.allocate
  end
end
