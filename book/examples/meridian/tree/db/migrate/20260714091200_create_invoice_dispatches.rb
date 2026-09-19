# frozen_string_literal: true

# SHARED DIRECTORY. Three worktrees each wrote a distinct filename here and git
# reported no conflict; the ordering between them is what nobody had run.
class CreateInvoiceDispatches < ActiveRecord::Migration[7.2]
  def change
    create_table :invoice_dispatches do |t|
      t.references :invoice, null: false, foreign_key: true
      t.string     :channel, null: false, default: "email"
      t.datetime   :dispatched_at
      t.jsonb      :provider_response, null: false, default: {}

      t.timestamps
    end

    add_index :invoice_dispatches, %i[invoice_id channel], unique: true
  end
end
