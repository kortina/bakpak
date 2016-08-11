require 'rspec'
require './foo'

RSpec.describe Foo do
  describe '#initialize' do
    it 'initializes with boo' do
      expect(Foo.new(1).boo).to eq 1
    end
  end

  describe '#pboo' do
    it 'prepends boo val with p' do
      expect(Foo.new(1).pboo).to eq 'p1'
    end
  end
end
