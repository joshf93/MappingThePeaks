<p>
This document discusses the implementation of the cInstruction and Genome classes.
</p>


<p>&nbsp;</p>
<h2>The cInstruction Class</h2>

<p>
This class is used to represent a single instruction within a genome.  The
private portion of this class consists of a single number that uniquely
identifies the type of instruction, and the public section
has a number of helper methods that allow us to work with that number.
</p>

<pre>
class <span class="class">cInstruction</span> {
private:
  unsigned char <span class="object">m_operand</span>;

public:
  <span class="comment">// Constructors and Destructor...</span>
  <span class="method">cInstruction</span>() : <span class="object">m_operand</span>(0) { ; }
  <span class="method">cInstruction</span>(const <span class="class">cInstruction</span>&amp; <span class="object">inst</span>) { *<span class="object">this</span> = <span class="object">inst</span>; }
  explicit <span class="method">cInstruction</span>(<span class="class">int</span> <span class="object">in_op</span>) { <span class="method">SetOp</span>(<span class="object">in_op</span>); }
  <span class="method">~cInstruction</span>() { ; }

  <span class="comment">// Accessors...</span>
  <span class="class">int</span> <span class="method">GetOp()</span> const { return static_cast&lt;int&gt;(<span class="object">m_operand</span>); }
  void <span class="method">SetOp</span>(<span class="class">int</span> <span class="object">in_op</span>) { <span class="method">assert</span>(<span class="object">in_op</span> &lt; 256); <span class="object">m_operand</span> = <span class="object">in_op</span>; }

  <span class="comment">// Operators...</span>
  void <span class="method">operator=</span>(const <span class="class">cInstruction</span>&amp; <span class="object">inst</span>) { <span class="object">m_operand</span> = <span class="object">inst</span>.<span class="object">m_operand</span>; }
  <span class="class">bool</span> <span class="method">operator==</span>(const <span class="class">cInstruction</span>&amp; <span class="object">inst</span>) const { return (<span class="object">m_operand</span> == <span class="object">inst</span>.<span class="object">m_operand</span>); }
  <span class="class">bool</span> <span class="method">operator!=</span>(const <span class="class">cInstruction</span>&amp; <span class="object">inst</span>) const { return !(<span class="method">operator==</span>(<span class="object">inst</span>)); }

  <span class="comment">// Some extra methods to convert too and from alpha-numeric symbols...</span>
  <span class="class">char</span> <span class="method">GetSymbol</span>() const;
  void <span class="method">SetSymbol</span>(<span class="class">char</span> <span class="object">symbol</span>);
};
</pre>

<p>
As stated above, the only private datum is a numerical value that identifies
this instruction.  The name <span class="object">m_operand</span> is the term
that is used for a command name in an assembly language.  Most normal assembly
languages have both an operand and arguments associated with each full command.
In Avida, the commands have no arguments, and hence they just consist of a
single operand.  The data type used for this is <code>unsigned char</code>.  A
char is an 8 bit number, so when one is unsigned, it represents a number from 0
to 255. As Avida is currently implemented, we are limited to 256 distinct
instructions.  To the outside world, we treat the instruction operand like an
integer, so it would be easy to modify this class were we ever to need more
than 256 instructions in the set.  The only reason to limit it to 8 bits
internally (rather than the 32 of an int) is to save memory when we have a very
large number of instructions throughout a population.  Instructions already
make up over half of all the memory resources used by Avida.
</p>
<p>
The public methods begin with the <span class="method">GetOp</span>() and
<span class="method">SetOp</span>() methods, which are standard accessors.
Next, we have a collection of methods that begin with the word 'operator'.
These are used to define how the corresponding symbols should be treated
when applied to objects of this class.  For example, the method 
<span class="method">operator==</span>() is called when we try to compare
an object of type cInstruction to another.  We have full control over the
definition of this method, just like any other.
</p>
<p>
Finally, we have a pair of methods that convert instructions to and from
alphanumeric characters (symbols). These methods are used to print instructions
out in a maximally compressed format, and to load them back in.  The order of
symbols used are the letters 'a' through 'z' in lowercase, followed by an
uppercase 'A' through 'Z' and finally the numbers '0' through '9'.  If there
are more than 62 possible instructions, all the rest are assigned a '?' when
printed out, and cannot be read back in properly from this format.
</p>


<p>&nbsp;</p>
<h2>The Genome class</h2>

<p>
A genome is a sequence of instructions.  The following class maintains this
sequence as an array, and provides a collection of methods to manipulate the
total construct.
</p>

<pre>
class <span class="class">Genome</span>
{
protected:
  <span class="class">Apto::Array</span>&lt;<span class="class">cInstruction</span>&gt; <span class="object">genome</span>;
  int <span class="object">active_size</span>;
 
public:
  <span class="method">Genome</span>() { ; }
  explicit <span class="method">Genome</span>(int <span class="object">_size</span>);
  <span class="method">Genome</span>(const <span class="class">Genome</span>&amp; <span class="object">in_genome</span>);
  <span class="method">Genome</span>(const <span class="class">cString</span>&amp; <span class="object">in_string</span>);
  virtual <span class="method">~Genome</span>();
 
  virtual void <span class="method">operator=</span>(const <span class="class">Genome</span>&amp; <span class="object">other_genome</span>);
  virtual bool <span class="method">operator==</span>(const <span class="class">Genome</span>&amp; <span class="object">other_genome</span>) const;
  virtual bool <span class="method">operator!=</span>(const <span class="class">Genome</span>&amp; <span class="object">other_genome</span>) const { return !(<span class="object">this</span>-&gt;<span class="method">operator==</span>(<span class="object">other_genome</span>)); }
  virtual bool <span class="method">operator&lt;</span>(const <span class="class">Genome</span>&amp; <span class="object">other_genome</span>) const { return <span class="method">AsString</span>() &lt; <span class="object">other_genome</span>.<span class="method">AsString</span>(); }
 
  <span class="class">cInstruction</span>&amp; <span class="method">operator[]</span>(int <span class="object">index</span>) { <span class="method">assert</span>(<span class="object">index</span> &gt;= 0 &amp;&amp; <span class="object">index</span> &lt; <span class="object">active_size</span>);  return <span class="object">genome</span>[<span class="object">index</span>]; }
  const <span class="class">cInstruction</span>&amp; <span class="method">operator[]</span>(<span class="class">int</span> <span class="object">index</span>) const { <span class="method">assert</span>(<span class="object">index</span> &gt;= 0 &amp;&amp; <span class="object">index</span> &lt; <span class="object">active_size</span>);  return <span class="object">genome</span>[<span class="object">index</span>]; }
 
  virtual void <span class="method">Copy</span>(int <span class="object">to</span>, int <span class="object">from</span>);
 
  int <span class="method">GetSize</span>() const { return <span class="object">active_size</span>; }
  <span class="class">cString</span> <span class="method">AsString</span>() const;
};
</pre>

<p>
The protected variable <span class="object">genome</span> is an array 
containing an object of type cInstruction at each position.  The second
variable <span class="object">active_size</span> denotes the number of
instructions in this array that are currently being used.  The fact that
these variables are "protected" instead of "private" means that any
class derived from <span class="class">Genome</span> will also have direct
access to the variables.  In particular, the class
<span class="class">cCPUMemory</span> extends Genome, adding methods to
alter the array length and new variables to keep track of information about
each instruction.
</p>
<p>
Three constructors allow for a new Genome object to be specified by either a
genome length, a previously created genome, or else a string -- a sequence
of symbols representing each instruction in order.
</p>
<p>
The operators created for manipulating genomes include both assignment 
(setting one genome equal to another) and comparison (testing to see if
two genomes are identical.)  Additionally, there are two
<span class="method">operator[]</span> methods.  This means that if you
have an object of type Genome, you can index into it to retrieve a single
instruction.  Thus, if the object was called <code>initial_genome</code>, the 
statement <code>initial_genome[15]</code> would return the instruction at
position fifteen in the genome. This occurs by calling one of these methods
with the appropriate integer. The difference between these two operator
methods is that one of them is for mutable genomes (i.e. those that can be
modified) -- a reference to the instruction in question is returned allowing
it to be altered. The other index operator (operator[] method) is for const
genomes, which can never be changed so only the value of the instruction is
returned.
</p>
<p>
The <span class="method">Copy(</span>) method is a shortcut to copy memory
from one position in the genome to another.  This method will later be
<strong>overloaded</strong> (that is, replaced with a newer version) by
cCPUMemory such that the proper flags will be copied, with the instruction
and others will be set to indicate the copied instruction for future tests.
<span class="method">GetSize</span>() returns the length of the genome, and
<span class="method">AsString</span>() returns a string who has symbols in
each position that correspond to the the instruction in the same position in
the genome.
</p>
