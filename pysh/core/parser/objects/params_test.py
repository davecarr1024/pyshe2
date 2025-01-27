# from pysh.core import regex
# from pysh.core.parser import Parser
# from pysh.core.parser.objects import Param, Params


# def test_combine(subtests):
#     int_ = Parser.head("int", regex.Regex.digits().one_or_more()).value().transform(int)
#     a: Param[int] = int_.param("a")
#     b: Param[int] = int_.param("b")
#     c: Param[int] = int_.param("c")
#     d: Param[int] = int_.param("d")
#     prefix: Param[int] = "a" & a
#     suffix: Param[int] = a & "a"
#     p: Params = a & b
#     for params in list[Params](
#         [
#             a & b & c & d,
#             (a & b) & c & d,
#             a & (b & c) & d,
#             a & b & (c & d),
#             (a & b) & (c & d),
#         ]
#     ):
#         with subtests.test(params=params):
#             assert params == Params.for_children(a, b, c, d)
