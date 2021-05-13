import pytest

def fuzzy_math(num1, operator, num2):
  if type(num1) != int or type(num2) != int:
    raise Exception('We need to do fuzzy math on ints')

  if operator == '+':
    result = num1 + num2
  elif operator == '*':
    result = num1 * num2
  else:
    raise Exception(f"I don't know how to do math with '{operator}'")

  if result < 0:
    return 'A negative number?'
  elif result < 10:
    return 'A small number'
  elif result < 20:
    return 'A medium number'
  else:
    return 'A really big number'


class TestFuzzyMath:
  
  def test_non_int_input_num1(self):
    with pytest.raises(Exception) as exc_info:
      fuzzy_math('he', '+', 2)
    assert 'fuzzy math on ints' in str(exc_info)

  def test_non_int_input_num2(self):
    pass

  def test_addition_with_negative_result(self):
    pass

  def test_addition_with_small_result(self):
    assert 'small number' in fuzzy_math(2, '+', 2)

  def test_addition_with_med_result(self):
    assert 'medium number' in fuzzy_math(12, '+', 2)

  def test_addition_with_large_result(self):
    assert 'really big' in fuzzy_math(22, '+', 22)
  
  def test_mult_with_negative_result(self):
    pass

  def test_mult_with_small_result(self):
    pass

  def test_mult_with_med_result(self):
    pass

  def test_mult_with_large_result(self):
    pass

  def test_invalid_operator(self):
    pass
