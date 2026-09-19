# meridian

Freight booking platform. Nineteen deployable services under `services/`, shared code under
`engines/`.

Shared files that no agent may touch concurrently: `config/routes.rb`, `db/migrate/`, and
`Gemfile.lock`.
