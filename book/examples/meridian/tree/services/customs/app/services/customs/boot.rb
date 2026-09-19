# frozen_string_literal: true

module Customs
  # Deployable service boundary. Wiring only; domain logic lives in app/.
  class Boot
    def self.call(env)
      Rack::Builder.app do
        map("/healthz") { run ->(_) { [200, { "content-type" => "text/plain" }, ["ok"]] } }
        run Customs::Router.new(env)
      end
    end
  end
end
