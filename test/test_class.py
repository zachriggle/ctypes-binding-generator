import unittest
import helper


class TestClass(helper.TestCtypesBindingGenerator):

    def test_class(self):
        self.run_test('''
class foo {
  private:
    int i;
  protected:
    int j;
  public:
    int k;
  protected:
    int l;
  private:
    int m;
};

typedef class {
  private:
    int x;
} bar;
        ''', '''
class foo(Structure):
    pass
foo._fields_ = [('i', c_int),
                ('j', c_int),
                ('k', c_int),
                ('l', c_int),
                ('m', c_int)]

class bar(Structure):
    pass
bar._fields_ = [('x', c_int)]
        ''', filename='input.cpp')


if __name__ == '__main__':
    unittest.main()