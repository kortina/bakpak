# Test class
class Foo
  attr_accessor :boo
  def initialize(boo)
    self.boo = boo
  end

  def pboo
    "p#{boo}"
  end
end
