#taken from speech-rule-engine
from __future__ import unicode_literals
import mathml_accessibility

tests = [
"""<math xmlns="http://www.w3.org/1998/Math/MathML">
  <mrow>
    <mn> 2 </mn>
    <mo> + </mo>
    <mrow>
      <mn> 3 </mn>
      <mo> &#x2062;<!--INVISIBLE TIMES--> </mo>
      <mi> &#x2148;<!--DOUBLE-STRUCK ITALIC SMALL I--> </mi>
    </mrow>
    <mfrac> <mn> 1 </mn> <mn> 2 </mn> </mfrac>
    <mi> &#x3C0;<!--GREEK SMALL LETTER PI--> </mi>
    <mi> &#x2147;<!--DOUBLE-STRUCK ITALIC SMALL E--> </mi>
    <mi> &#x1F111;<!--Surrogate Pair--> </mi>
  </mrow>
</math>
""", """
<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
<mrow>
  <mi>x</mi>
  <mo>=</mo>
  <mfrac>
    <mrow>
      <mo>&#x2212;</mo>
      <mi>b</mi>
      <mo>&#xB1;</mo>
      <msqrt>
        <mrow>
          <msup>
            <mi>b</mi>
            <mn>2</mn>
          </msup>
          <mo>&#x2212;</mo>
          <mn>4</mn>
          <mi>a</mi>
          <mi>c</mi>
        </mrow>
      </msqrt>
    </mrow>
    <mrow>
      <mn>2</mn>
      <mi>a</mi>
    </mrow>
  </mfrac>
</mrow>
</math>
""", """
<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
<mstyle>
  <mi>f</mi>
  <mrow>
    <mo>(</mo>
    <mi>a</mi>
    <mo>)</mo>
  </mrow>
  <mo>=</mo>
  <mfrac>
    <mn>1</mn>
    <mrow>
      <mn>2</mn>
      <mi>&#x3C0;</mi>
      <mi>i</mi>
    </mrow>
  </mfrac>
  <msub>
    <mo>&#x222E;</mo>
    <mrow>
      <mi>&#x3B3;</mi>
    </mrow>
  </msub>
  <mfrac>
    <mrow>
      <mi>f</mi>
      <mo>(</mo>
      <mi>z</mi>
      <mo>)</mo>
    </mrow>
    <mrow>
      <mi>z</mi>
      <mo>&#x2212;</mo>
      <mi>a</mi>
    </mrow>
  </mfrac>
  <mi>d</mi>
  <mi>z</mi>
</mstyle>
</math>
""", """
<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
<mrow>
  <mi>&#x3C3;</mi>
  <mo>=</mo>
  <msqrt>
    <mrow>
      <mfrac>
        <mrow>
          <mn>1</mn>
        </mrow>
        <mrow>
          <mi>N</mi>
        </mrow>
      </mfrac>
      <mstyle displaystyle="true">
        <mrow>
          <munderover>
            <mrow>
              <mo>&#x2211;</mo>
            </mrow>
            <mrow>
              <mi>i</mi>
              <mo>=</mo>
              <mn>1</mn>
            </mrow>
            <mrow>
              <mi>N</mi>
            </mrow>
          </munderover>
          <mrow>
            <msup>
              <mrow>
                <mo stretchy="false">(</mo>
                <msub>
                  <mrow>
                    <mi>x</mi>
                  </mrow>
                  <mrow>
                    <mi>i</mi>
                  </mrow>
                </msub>
                <mo>&#x2212;</mo>
                <mi>&#x3BC;</mi>
                <mo stretchy="false">)</mo>
              </mrow>
              <mrow>
                <mn>2</mn>
              </mrow>
            </msup>
          </mrow>
        </mrow>
      </mstyle>
    </mrow>
  </msqrt>
  <mo>.</mo>
</mrow>
</math>
"""]

for i in tests:
	print mathml_accessibility.translate(i).encode("raw_unicode_escape")
