<p>
This document discusses how to implement your own tasks to use as triggers
for reactions in the environment.
</p>


<p>&nbsp;</p>
<h2>1. Build the prototype of the method that will be used to test the new task</h2>

<p>
For this step, you will be editing the task library found in the files
<kbd>cTaskLib.cc</kbd> and <kbd>cTaskLib.h</kbd> in the directory
<kbd>source/main/</kbd>.  Start by adding the prototype of your new test
function to the cTaskLib class in the header file.  The data that will be
tested is all stored within task context that is passed into this function.
This function will output a double that represents the <em>quality</em> with
which the task is performed.  This is a number between 0 and 1 that
determines the fraction of the bonus that should be received.  For tasks that
are either successful or not, this will only return 0.0 or 1.0.
</p>
<p>
For example, if we were going to create a task that tests if the organisms
could double one of their inputs, we might call that task 'times2'.  We would
then add the line to this file:
</p>
<pre>
double <span class="method">Task_Times2</span>(<span class="class">cTaskContext</span>& <span class="object">ctx</span>) const;
</pre>

<p>
If possible, place it near other tasks of the same type.  In this case,
I choose to place it directly after Task_Echo(), since this is also an
easy task for the organisms to perform.
</p>


<p>&nbsp;</p>
<h2>2. Build the body of the method that will be used to test the new task</h2>

<p>
We next go into the code (<kbd>cTaskLib.cc</kbd>) file, and add the body of our
new method.  We search for cTaskLib::Task_Echo(), since our new prototype
followed this method in the header file, and place the body of our function
immediately after it.
</p>

<pre>
double <span class="class">cTaskLib</span>::<span class="method">Task_Times2</span>(<span class="class">cTaskContext</span>& <span class="object">ctx</span>) const
{
  const <span class="class">tBuffer</span><<span class="class">int</span>>& <span class="method">input_buffer</span> = <span class="object">ctx.</span><span class="method">GetInputBuffer</span>();
  const <span class="class">int </span><span class="object">test_output</span> = <span class="object">ctx</span>.<span class="method">GetOutputBuffer</span>()[0];
  const <span class="class">int</span> <span class="object">input_size</span> = <span class="object">ctx</span>.<span class="method">GetInputBuffer</span>().<span class="method">GetNumStored</span>();
  for (<span class="class">int</span> <span class="object">i</span> = 0; <span class="object">i</span> < <span class="object">input_size</span> ; <span class="object">i</span>++)
  {
    if ( <span class="object">test_output</span> == 2 * <span class="object">input_buffer</span>[<span class="object">i</span>])
    {
      return 1.0;
    }
  }
  return 0.0;
}
</pre>

<p>
The most recent output is always placed at the beginning of the output
buffer, so we store it in the variable
<span class="object">test_output</span> to compare it against all of the
different inputs.  We then have a for-loop that goes from 0 to the number
of inputs stored in the input buffer.  Inside the body of the loop, we
test for each input if twice that input is equal to the output.  If so,
then the task was successful and we return a 1.0.  If all of the tests
fail and we exit the loop, then we return a 0.0.
</p>
<p>
These test methods should be carefully written so that they run as fast
as possible.  In particular, if a task requires that an output be
compared to multiple inputs at a time (i.e., the tasks Add or Subtract),
then this can become combinartoically explosive.  For the moment, we
keep control on this problem by only allowing three different inputs
in the input buffer, but in the future this number may need to become
higher.
</p>


<p>&nbsp;</p>
<h2>3. Attach our new method to the name of its trigger</h2>

<p>
This next step is also done in the code file, inside the
<span class="class">cTaskLib</span>::<span class="method">AddTask</span>()
method.  Again, we want this to be in the same place, so we locate the
task 'echo' that its supposed to follow, and add in the new line.
</p>

<pre>
else if (<span class="object">name</span> == &quot;times2&quot;)
  <span class="method">NewTask</span>(<span class="object">name</span>, &quot;Times2&quot;, &amp;<span class="class">cTaskLib</span>::<span class="method">Task_Times2</span>);
</pre>    

<p>
This line will attach the name to the description &quot;Times2&quot; (which
could have been a little more detailed, but should be 40 characters or less)
as well as the function that should be called when that name is listed as a
trigger to a reaction.
</p>
<p>
You are now ready to use your task!
</p>
