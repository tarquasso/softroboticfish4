manchester = [
  "01",
  "10",
]

manchester4 = [
  "0101",
  "0110",
  "1001",
  "1010",
]

mycode = [
  "10001101",
  "01110010",
]

codes154 = [
  "11011001110000110101001000101110",
  "11101101100111000011010100100010",
  "00101110110110011100001101010010",
  "00100010111011011001110000110101",
  "01010010001011101101100111000011",
  "00110101001000101110110110011100",
  "11000011010100100010111011011001",
  "10011100001101010010001011101101",
  "10001100100101100000011101111011",
  "10111000110010010110000001110111",
  "01111011100011001001011000000111",
  "01110111101110001100100101100000",
  "00000111011110111000110010010110",
  "01100000011101111011100011001001",
  "10010110000001110111101110001100",
  "11001001011000000111011110111000",
]

c2t = {
  "00": (-1-1j),
  "01": (-1+1j),
  "10": ( 1-1j),
  "11": ( 1+1j),
}
t2c = dict (zip(c2t.values(),c2t.keys()))

def bitflip(n, bits):
  ind = 0
  for i in range(bits):
    ind <<= 1
    if n & 1:
      ind += 1
    n >>= 1
  return ind

def codes2table(c):
  table = []
  bits = len(bin(len(c)))-3
  for n in range(len(c)):
    code = c[bitflip(n, bits)]
    for pair in [code[i:i+2] for i in range(0, len(code), 2)]:
      table.append(c2t[pair])
  return table

def table2codes(t, l):
  c = [[]]*l
  for n, code in enumerate([t[i:i+l] for i in range(0, len(t), l)]):
    s = ""
    for pair in code:
      s += t2c[pair]
    c[bitflip(n, len(bin(l))-3)] = s
  return c

def codes2corr(c, sps):
  corr = []
  for code in c:
    cc = []
    for chip in code:
      cc.extend(([-1] if chip=="0" else [1])*sps)
    corr.append(cc)
  return corr

if __name__ == "__main__":
  t1 = codes2table(codes154)
  t2 = [(1+1j), (-1+1j), (1-1j), (-1+1j), (1+1j), (-1-1j), (-1-1j), (1+1j), (-1+1j), (-1+1j), (-1-1j), (1-1j), (-1-1j), (1-1j), (1+1j), (1-1j), (1-1j), (-1-1j), (1+1j), (-1-1j), (1-1j), (-1+1j), (-1+1j), (1-1j), (-1-1j), (-1-1j), (-1+1j), (1+1j), (-1+1j), (1+1j), (1-1j), (1+1j), (-1+1j), (-1+1j), (-1-1j), (1-1j), (-1-1j), (1-1j), (1+1j), (1-1j), (1+1j), (-1+1j), (1-1j), (-1+1j), (1+1j), (-1-1j), (-1-1j), (1+1j), (-1-1j), (-1-1j), (-1+1j), (1+1j), (-1+1j), (1+1j), (1-1j), (1+1j), (1-1j), (-1-1j), (1+1j), (-1-1j), (1-1j), (-1+1j), (-1+1j), (1-1j), (-1-1j), (1-1j), (1+1j), (1-1j), (1+1j), (-1+1j), (1-1j), (-1+1j), (1+1j), (-1-1j), (-1-1j), (1+1j), (-1+1j), (-1+1j), (-1-1j), (1-1j), (-1+1j), (1+1j), (1-1j), (1+1j), (1-1j), (-1-1j), (1+1j), (-1-1j), (1-1j), (-1+1j), (-1+1j), (1-1j), (-1-1j), (-1-1j), (-1+1j), (1+1j), (1+1j), (-1-1j), (-1-1j), (1+1j), (-1+1j), (-1+1j), (-1-1j), (1-1j), (-1-1j), (1-1j), (1+1j), (1-1j), (1+1j), (-1+1j), (1-1j), (-1+1j), (1-1j), (-1+1j), (-1+1j), (1-1j), (-1-1j), (-1-1j), (-1+1j), (1+1j), (-1+1j), (1+1j), (1-1j), (1+1j), (1-1j), (-1-1j), (1+1j), (-1-1j), (1+1j), (1-1j), (1+1j), (-1+1j), (1-1j), (-1+1j), (1+1j), (-1-1j), (-1-1j), (1+1j), (-1+1j), (-1+1j), (-1-1j), (1-1j), (-1-1j), (1-1j), (1-1j), (1+1j), (1-1j), (-1-1j), (1+1j), (-1-1j), (1-1j), (-1+1j), (-1+1j), (1-1j), (-1-1j), (-1-1j), (-1+1j), (1+1j), (-1+1j), (1+1j), (-1-1j), (1+1j), (-1+1j), (-1+1j), (-1-1j), (1-1j), (-1-1j), (1-1j), (1+1j), (1-1j), (1+1j), (-1+1j), (1-1j), (-1+1j), (1+1j), (-1-1j), (-1+1j), (1-1j), (-1-1j), (-1-1j), (-1+1j), (1+1j), (-1+1j), (1+1j), (1-1j), (1+1j), (1-1j), (-1-1j), (1+1j), (-1-1j), (1-1j), (-1+1j), (-1-1j), (1-1j), (-1-1j), (1-1j), (1+1j), (1-1j), (1+1j), (-1+1j), (1-1j), (-1+1j), (1+1j), (-1-1j), (-1-1j), (1+1j), (-1+1j), (-1+1j), (-1+1j), (1+1j), (-1+1j), (1+1j), (1-1j), (1+1j), (1-1j), (-1-1j), (1+1j), (-1-1j), (1-1j), (-1+1j), (-1+1j), (1-1j), (-1-1j), (-1-1j), (1-1j), (-1+1j), (1+1j), (-1-1j), (-1-1j), (1+1j), (-1+1j), (-1+1j), (-1-1j), (1-1j), (-1-1j), (1-1j), (1+1j), (1-1j), (1+1j), (-1+1j), (1+1j), (-1-1j), (1-1j), (-1+1j), (-1+1j), (1-1j), (-1-1j), (-1-1j), (-1+1j), (1+1j), (-1+1j), (1+1j), (1-1j), (1+1j), (1-1j), (-1-1j)]

  eq = [x == y for (x,y) in zip(t1,t2)]
  print all(eq)

  c2 = table2codes(t2,16)
  eq = [x == y for (x,y) in zip(codes154,c2)]
  print all(eq)

  for i,x in enumerate(c2):
    print i, hex(int(x,2))

