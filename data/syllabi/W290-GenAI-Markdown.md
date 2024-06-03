# DATASCI 290: Generative AI - Foundations, Techniques, Challenges, and Opportunities

[Course Overview](#course-overview)  
[Course Evaluation](#course-evaluation)  
[Course Resources](#course-resources)  
[Tentative Schedule and Readings](#tentative-schedule-and-readings)


## Course Overview

**Course Description**

Recent developments in neural network architectures, algorithms, and computing hardware have led to a revolutionary development usually referred to as Generative AI nowadays. Large Language Models (LLMs) are now able to generate seemingly human-like text in response to tasks like summarization, question answering, etc with high level of accuracy. Leveraging similar strategies, comparable advances have been made with images as well as audio.  With today’s (and anticipated future) capabilities, Generative AI is poised to be a tool used comprehensively in a wide variety of ways, and therefore to have a profound set of effects on our lives and society as a whole. 

This course is a broad introduction to these new technologies. It is split conceptually into three parts. In the Introduction section we will cover the historical aspects, key ideas and learnings all the way to Transformer architectures and training aspects. In the Practical Aspects and Techniques section, we will learn how to deploy, use, and train LLMs. We will discuss core concepts like prompt tuning, quantization, and parameter efficient fine-tuning, and we will also explore use case patterns. Finally, we will discuss challenges & opportunities offered by Generative AI, where we will highlight critical issues like bias and inclusivity, fake information, and safety, as well as some IP issues.

Our focus will be on practical aspects of LLMs to enable students to be both effective and responsible users of generative AI technologies.



**Course Prerequisites**

* [MIDS 207 (Machine Learning)](https://www.ischool.berkeley.edu/courses/datasci/207): We assume you know what gradient descent is.  We review simple linear classifiers and softmax at a high level, but make sure you've at least heard of these! You should also be comfortable with linear algebra, which we use for vector representations and when we discuss deep learning.
* Strong coding capabilities in Python are a prerequisite. All assignments and notebooks will be based on Python. 
* PyTorch will be our core framework. Prior familiarity is a plus, but not required. A targeted overview of PyTorch will be provided in the early part of the course. 
* Time:  There are four to five substantial assignments in this course, with the final one taking up the final four weeks.  Make sure you give yourself enough time to be successful! In particular, you may be in for a rough semester if you have other significant commitments at work or home, or take both this course and any of 210 (Capstone), 261, or 271.


**Course Goals and Objectives**

By the completion of this course, students will:

* Appreciate the history of the path towards Large Language Models (LLMs) and Generative AI approaches.
* Understand the foundations of LLMs, how they are trained, and how to deploy and use them, for and beyond text-focused problems.
* Be able to understand key use case patterns of Generative AI approaches and know how to think about incorporating them into applications.
* Become conversant in PyTorch and key neural net coding strategies.
* Know how to approach improving the results obtained from LLMs through prompt-tuning, instruction-based fine-tuning, and Reinforcement Learning with Human Feedback.
* Become aware of critical issues such as bias, inclusivity problems, hallucinations, and IP questions



**Communication and Resources**

* Course website: [GitHub MIDS-GAI290/2024-spring](../../../)
* [Ed Discussion](https://https://bcourses.berkeley.edu/courses/1531220): We'll use this for collective Q&A, and this will be the fastest way to reach the course staff. Note that you can post anonymously, or make posts visible only to instructors for private questions.
* Email list for course staff (expect a somewhat slower response here): [mids-gen-ai-instructors@googlegroups.com](mailto:mids-gen-ai-instructors@googlegroups.com)


**Live Sessions**
* Section 1: Tuesday 4:00 - 5:30pm PST (Mark Butler) 
* Section 2: Tuesday 6:30 - 8:00pm PST (Joachim Rahmfeld)
* Section 3: Wednesday 6:30 - 8:00pm PST (Mark Butler)
* **ALL** Sections : Friday 4:00 - 5:30pm PST (Both)



**Teaching Staff Office Hours**

* **Joachim Rahmfeld**: Thursday at noon PST
* **Mark Butler**: Wednesday at 4:00 pm PST
* **Rich Robbins**: Thursday at 4:00 pm PST


Office hours are for the whole class; students from any section are welcome to attend any of the times above.


## Course Evaluation

### Deliverables Breakdown

<table>
<tr>
<th>Assignment</th><th>Topic</th><th>Release</th><th>Deadline</th><th>Weight</th>
</tr>
<tr>
  <td>
  <!-- <strong><a href="../assignment/a0" target="_blank">Assignment&nbsp;0</a></strong>  -->
  Assignment&nbsp;0
  <td><strong>Course Set Up</strong>
  <ul>
    <li>GitHub
    <li>Ed Discussion
    <li>Google Colab Pro
  </ul></td>
  <td>Jan&nbsp;16</td>
  <td>Jan&nbsp;21</td>
  <td>0%</td>
</tr>
<tr>
  <td>
  <!-- <strong><a href="../assignment/a1" target="_blank">Assignment&nbsp;1</a></strong>  -->
  Assignment&nbsp;1
  <td><strong>PyTorch Basics, HuggingFace, and a Simple Application: Sentence Classification</strong></td>
  <td>Jan&nbsp;19</td>
  <td>Feb&nbsp;04</td>
  <td>15%</td>
</tr>
<tr>
  <td>
  <!-- <strong><a href="../assignment/a3" target="_blank">Assignment&nbsp;3</a></strong>  -->
  Assignment&nbsp;2
  <td><strong>GPT-2: Evaluation of pre-trained and fine-tuned models</strong></td>
  <td>Feb&nbsp;02</td>
  <td>Feb&nbsp;18</td>
  <td>15%</td>
</tr>
<tr>
  <td>
  <!-- <strong><a href="../assignment/a2" target="_blank">Assignment&nbsp;2</a></strong>  -->
  Assignment&nbsp;3
  <td><strong>Image Generation and Evaluation</strong></td>
  <td>Feb&nbsp;16</td>09
  <td>Feb&nbsp;25</td>
  <td>10%</td>
</tr>

<tr>
  <td>
  <!-- <strong><a href="../assignment/a4" target="_blank">Assignment&nbsp;4</a></strong>  -->
  Assignment&nbsp;4
  <td><strong>Prompt Engineering</strong></td>
  <td>Feb&nbsp;23</td>
  <td>Mar&nbsp;10</td>
  <td>20%</td>
</tr>
<tr>
  <td>
  <!-- <strong><a href="../assignment/a0" target="_blank">Assignment&nbsp;0</a></strong>  -->
  Final Assignment
  <td><strong>Building a Retrieval-Augmented Q&A System</strong></td>
  <td>Mar&nbsp;14</td>
  <td>Apr&nbsp;08</td>
  <td>40%</td>
</tr>
</table>

We will make an announcement on Ed Discussion when grades are available.



### General Grading Philosophy

The grading will be based on the Homework (60% combined) and the Final Assignment (40%).

As mentioned above, this course is a lot of work.  Give it the time it deserves and you'll be rewarded intellectually and on your transcript.


### Late Submission Policy

We recognize that sometimes things happen in life outside the course, especially in MIDS where we all have full-time jobs and family responsibilities to attend to. To help with these situations, we are giving you **5 "late days"** to use throughout the term as you see fit.  Each late day gives you a 24-hour (or any part thereof) extension to any deliverable in the course **except** the final project presentation or report. (UC Berkeley needs grades submitted very shortly after the end of classes.)

Once you run out of late days, each 24-hour period (or any part thereof) results in a **10 percentage-point deduction** on that deliverable's grade.

You can use a **maximum of 2 late days** on any single deliverable.  We will **not be accepting any submissions more than 48 hours past the original due date**, even if you have late days. (We want to be more flexible here, but your fellow students also want their graded assignments back promptly!)

We don't anticipate granting extensions beyond these policies.  Plan your time accordingly!

### More Serious Issues

If you run into a more serious issue that will affect your ability to complete the course, please email the instructors mailing list and cc MIDS Student Services.  A word of warning: In previous sections, we have had students ask for an Incomplete (INC) grade because their lives were otherwise busy.  Mostly we have declined, opting instead for the student to complete the course to the best of their ability and have a grade assigned based on that work.  (MIDS prefers to avoid giving INCs, as they have been abused in the past.)  The sooner you start this process, the more options we (and the department) have to help.  Don't wait until you're suffering from the consequences to tell us what's going on!


### Collaboration Policy/Academic Integrity

All students —undergraduate, graduate, professional full time, part time, law, etc.— must be familiar with and abide by the provisions of the "Student Code of Conduct" including those provisions relating to Academic Misconduct. All forms of academic misconduct, including cheating, fabrication, plagiarism or facilitating academic dishonesty will not be tolerated. The full text of the UC Berkeley Honor Code is available at:  https://teaching.berkeley.edu/berkeley-honor-code and the Student Code of Conduct is available at: https://sa.berkeley.edu/student-code-of-conduct#102.01_Academic_Misconduct

We encourage studying in groups of two to four people. This applies to working on homework, discussing labs and projects, and studying. However, students must always adhere to the UC Berkeley Code of Conduct (http://sa.berkeley.edu/code-of-conduct ) and the UC Berkeley Honor Code (https://teaching.berkeley.edu/berkeley-honor-code ). In particular, all materials that are turned in for credit or evaluation must be written solely by the submitting student. Similarly, you may consult books, publications, or online resources to help you study. In the end, you must always credit and acknowledge all consulted sources in your submission (including other persons, books, resources, etc.)


## Attendance and Participation

We believe in the importance of the social aspects of learning —between students, and between students and instructors— and we recognize that knowledge-building does not solely occur on an individual level, but is built by social activity involving people and by members engaged in the activity. Participation and communication are key aspects of this course vital to the learning experiences of you and your classmates.

Therefore, we like to remind all students of the following requirements for live class sessions:

* Students are required to join live class sessions from a study environment with video turned on and with a headset for clear audio, without background movement or background noise, and with an internet connection suitable for video streaming.

* You are expected to engage in class discussions, breakout room discussions and exercises, and to be present and attentive for your and other teams’ in-class presentations. 

* Keep your microphone on mute when not talking to avoid background noise. Do your best to minimize distractions in the background video, and ensure that your camera is on while you are engaged in discussions. 

That said, in exceptional circumstances, if you are unable to meet in a space with no background movement, or if your connection is poor, make arrangements with your instructor (beforehand if possible) to explain your situation. Sometimes connections and circumstances make turning off video the best option. If this is a recurring issue in your study environment, you are responsible for finding a different environment that will allow you to fully participate in classes, without distraction to your classmates.

**Failure to adhere to these requirements will result in an initial warning from your instructor(s), followed by a possible reduction in grades or a failing grade in the course.**


## Diversity and Inclusion

Integrating a diverse set of experiences is important for a more comprehensive understanding of data science. We make an effort to read papers and hear from a diverse group of practitioners. Still, limits exist on this diversity in the field of data science. We acknowledge that it is possible that there may be both overt and covert biases in the material due to the lens through which it was created. We would like to nurture a learning environment that supports a diversity of thoughts, perspectives and experiences, and honors your identities (including race, gender, class, sexuality, religion, ability, veteran status, etc.) in the spirit of the UC Berkeley Principles of Community https://diversity.berkeley.edu/principles-community

To help us accomplish this, please contact us or submit anonymous feedback through I School channels if you have any suggestions to improve the quality of the course. If something was said in class (by anyone) or you experience anything that makes you feel uncomfortable, please talk to your instructors about it. If you feel like your performance in the class is being impacted by experiences outside of class, please don’t hesitate to come and talk with us. We want to be a resource for you. Also, anonymous feedback is always an option and may lead us to make a general announcement to the class, if necessary, to address your concerns. As a participant in teamwork and course discussions, you should also strive to honor the diversity of your classmates.

If you prefer to speak with someone outside of the course, the MIDS Academic Director Drew Paulin, the I School Assistant Dean of Academic Programs Catherine Cronquist Browning, and the UC Berkeley Office for Graduate Diversity are excellent resources. Also see the following: https://www.ischool.berkeley.edu/about/community.

## Disability Services and Accommodations

If you need disability-related accommodations in this class, if you have emergency medical information you wish to share with me, or if you need special arrangements in case the building must be evacuated, please inform me as soon as possible.

The I School recognizes disability in the context of diversity, and the Disabled Students’ Program (DSP) equips students with appropriate accommodations and services to remove barriers to educational access. Students seeking accommodations in this class are responsible for completing the DSP application process to obtain an accommodation letter. You may reach the DSP at (510) 642-0518, or visit the website: https://dsp.berkeley.edu
 
## Publishing Your Work

You are highly encouraged to use your program coursework to build an academic/professional portfolio. 

* Blog about your coursework (and other ideas) and share on the I School Medium channel
  * Instructions are here on the intranet for students: https://www.ischool.berkeley.edu/intranet/connect 
  * Instructions here are public for alumni: https://www.ischool.berkeley.edu/alumni/stay-connected
* Publish projects to your I School project portfolio gallery (for more than just the capstone).
* Publish your work on LinkedIn and tag @UC Berkeley School of Information. Do **NOT** publish your homework assignments!
* Publish in academic journals: Contact your professors for assistance. (Note that multiple review iterations are usually required; this can be a time-intensive endeavor.)
  * For help writing professional academic papers students are encouraged to contact Sabrina Soracco, the Director of the Graduate Writing Center, in the Graduate Division -- see https://grad.berkeley.edu/staff/sabrina-soracco/ and https://grad.berkeley.edu/professional-development/graduate-writing-center/ -- the latter has links to resource guides, appointments with consultants, workshops, etc.
* Publish your news (e.g., conference talks, awards, scholarships) to the I School internal newsletter.

## Computing Costs

To apply the knowledge and skills covered in this course, students will be required to have access to [Google CoLab Pro](https://colab.research.google.com/signup). ($10 per month). We also expect that students will incur an estimated cost of $50 for access to ChatGPT [API and services](https://openai.com/pricing#language-models). during the term. Students are responsible for covering these costs, and for setting up accounts and access to these tools and services. More information will be provided about access to these tools early in the term.

## Course Resources

We are not using any particular textbook for this course. We’ll list some relevant readings each week. 
* [Deep Learning](http://www.deeplearningbook.org/) (Goodfellow, Bengio, and Courville)

We’ll be posting materials to the course [GitHub repo](../../../).

*Note:* This syllabus may be subject to change. We'll be sure to announce anything major on Ed Discussion.

### Code References

The course will be taught in Python, and we'll be making heavy use of NumPy, PyTorch, and Jupyter (IPython) notebooks via Colab Pro. We'll also be using Git for distributing and submitting materials. If you want to brush up on any of these, we recommend:
* **Git tutorials:** [Introduction / Cheat Sheet](https://git-scm.com/docs/gittutorial), or [interactive tutorial](https://try.github.io/)
* **Python / NumPy:** Stanford's CS231n has [an excellent tutorial](http://cs231n.github.io/python-numpy-tutorial/).
* **PyTorch:** We'll go over some basics of PyTorch in [Assignment 1](../../../tree/master/assignment/a1/).

  **Datasci 207:** [Python machine learning : machine learning and deep learning with python, scikit-learn, and pytorch](https://search.library.berkeley.edu/discovery/fulldisplay?docid=cdi_safari_books_v2_9781801819312&context=PC&vid=01UCS_BER:UCB&lang=en&search_scope=DN_and_CI&adaptor=Primo%20Central&tab=Default_UCLibrarySearch&query=creator,exact,Raschka,%20Sebastian,AND&facet=creator,exact,Raschka,%20Sebastian&mode=advanced&offset=10) by Raschka and Mirjalili is used (the TensorFlow version) in 207 and available to Berkeley students from the library.


### Miscellaneous Deep Learning and Gen AI/NLP References
Here are a few useful resources and papers that don’t fit under a particular week -- all optional, but interesting!
* (Optional) [Chris Olah’s blog](http://colah.github.io/) and [Distill](https://distill.pub/)
* (Optional) [GloVe: Global Vectors for Word Representation (Pennington, Socher, and Manning, 2014)](http://nlp.stanford.edu/pubs/glove.pdf)
* (Optional) [Lillian Weng's Blog](https://lilianweng.github.io/)
* (Optional) [Jack Clark's Import AI site](https://jack-clark.net/)
* (Optional) [Simon Willison's blog](https://simonwillison.net/)
* (Optional) [Jay Alammar’s blog](https://jalammar.github.io/) 
---

## Tentative Schedule and Readings

We'll update the table below with assignments as they become available, as well as additional materials throughout the semester. Keep an eye on GitHub for updates!

*Dates are tentative:* Assignments in particular may change topics and dates.  (Updated slides for each week will be posted during the live session week.)

### Live Session Slides [[available with @berkeley.edu address](https://drive.google.com/drive/folders/1gxOE7QetLpNSq9iOaMCaNQ_do5et38wg?usp=sharing)]

### Deliverables

Note:  we will update this table as we release assignments.  Each assignment
will be released around the last live session of the week and due approximately 1 week later (for simple assignments) or 2 to 3 weeks later (for complex assignments).

<table>
<tr>
<th></th><th>Topic</th><th>Release</th><th>Deadline</th>
</tr>
<tr>
  <td>
  <!-- <strong><a href="../assignment/a0" target="_blank">Assignment&nbsp;0</a></strong>  -->
  Assignment&nbsp;0
  <td><strong>Course Set-up</strong>
  <ul>
    <li>GitHub
    <li>Ed Discussion
  </ul></td>
  <td>Jan&nbsp;16</td>
  <td>Jan&nbsp;21</td>
</tr

<tr> <!-- a1 -->
  <td><strong><a href="../assignment/a1" target="_blank">Assignment&nbsp;1</a></strong>
  <td><strong>Assignment&nbsp;1</strong>
  <ul>
    <li>PyTorch &amp; Language Models
  </ul></td>
  <td>Jan&nbsp;19</td>
  <td>Feb&nbsp;04</td>
</tr>

<tr> <!-- a2 -->
  <td><strong><a href="../assignment/a2" target="_blank">Assignment&nbsp;2</a></strong>
  <td><strong>Assignment&nbsp;2</strong>
  <ul>
    <li>Pre-training &amp; Fine-tuning of Language Models
  </ul></td>
  <td>Feb&nbsp;02</td>
  <td>Feb&nbsp;18</td>
</tr>

<tr> <!-- a3 -->
  <td><strong><a href="../assignment/a3" target="_blank">Assignment&nbsp;3</a></strong>
  <td><strong>Assignment&nbsp;3</strong>
  <ul>
    <li>Image Generation and Evaluation
  </ul></td>
  <td>Feb&nbsp;16</td>
  <td>Feb&nbsp;25</td>
</tr>

<tr> <!-- a4 -->
  <td><strong><a href="../assignment/a4" target="_blank">Assignment&nbsp;4</a></strong>
  <td><strong>Assignment&nbsp;4</strong>
  <ul>
    <li>Prompt Engineering
  </ul></td>
  <td>Feb&nbsp;23</td>
  <td>Mar&nbsp;10</td>
</tr>

<tr> <!-- a5 -->
  <td><strong><a href="../assignment/a5" target="_blank">Assignment&nbsp;5</a></strong>
  <td><strong>Assignment&nbsp;5</strong>
  <ul>
    <li>Retrieval Augmented Generation
  </ul></td>
  <td>Mar&nbsp;14</td>
  <td>Apr&nbsp;08</td>
</tr>


</table>


### Course Schedule

<table>
<tr>
<th></th>
<th>Async Material to Watch</th>
<th>Topics</th>
<th>Materials</th>
</tr>

<tr><td></td><td><strong>Part I: Introduction</strong></td><td></td><td></td></tr>

<tr><!--- Introductions -->
  <td><strong>Week&nbsp;1</strong><br>(Jan&nbsp;08)</td>
  <td>How did we get here? And where are we, really?
  </td>
  <td><ul>
    <li>Course overview
<li>History of AI 
<li>AI & Neural Nets
<li>Neural Nets & Language
<li>Language and Reasoning
<li>LLMs as a Black Box... 
<li>Are we done?

  </ul></td>
  <td>
	<ul>
	  <li>Read: <a href="https://aima.cs.berkeley.edu/4th-ed/pdfs/newchap01.pdf" target="_blank">Artificial Intelligence: A Modern Approach, 4th US ed., Introduction</a>
	  <li>Read: <a href="https://jalammar.github.io/illustrated-bert/" target="_blank">The Illustrated BERT, ELMo, and co. (How NLP Cracked Transfer Learning)</a>
	  <li>Review: <a href="https://search.library.berkeley.edu/discovery/fulldisplay?docid=alma9914824770906531&context=L&vid=01UCS_BER:UCB&lang=en&search_scope=DN_and_CI&adaptor=Local%20Search%20Engine&tab=Default_UCLibrarySearch&query=any,contains,Python%20Machine%20Learning:%20Machine%20Learning%20and%20Deep%20Learning%20with%20Python&offset=0" target="_blank">Python machine learning : machine learning and deep learning with python, scikit-learn, and tensorflow 2 by Raschka and Mirjalili</a> [Chapters 11, 14, 15 for Neural Nets &amp; Chapters 12, 13, 16 for PyTorch]
	  <li>Review: <a href="http://playground.tensorflow.org/" target="_blank">Neural Net Playground</a>
	  <li>Skim: <a href="https://arxiv.org/pdf/2311.02462.pdf" target="_blank">Levels of AGI: Operationalizing Progress on the Path to AGI</a>
	  <li>Skim: <a href="https://arxiv.org/pdf/2307.10169.pdf" target="_blank">Challenges and Applications of Large Language Models</a>
  </ul>
</td>
</tr>

<tr><!--- Week 2 -->
  <td><strong>Week&nbsp;2</strong><br>(Jan&nbsp;15)</td>
  <td>
  <br>At the heart of it all: Context, context, context... (in language)
  </td>
  <td><ul>
  <li>The importance of context, a first look: 
<ul>
	<li>word embeddings trained from context
	<li>ANYTHING can be represented as a vector given context
	<li>limitations of word embeddings -> RNNs
	<li>limitations of RNNs -> Transformers
</ul>
  </ul></td>
  <td><ul>
	<li>Read: <a href="http://jalammar.github.io/illustrated-word2vec/" target=_blank">The Illustrated Word2Vec</a>
	<li>Skim: <a href="https://aclanthology.org/2022.acl-long.62.pdf" target=_blank">Language-agnostic BERT Sentence Embedding</a>
	<li>Skim: <a href="https://aclanthology.org/D19-1410.pdf" target=_blank">Augmented SBERT: Data Augmentation Method for Improving Bi-Encoders for Pairwise Sentence Scoring Tasks</a>
	<li>Skim: <a href="https://txt.cohere.com/embedding-archives-wikipedia/" target=_blank">The Embedding Archives: Millions of Wikipedia Article Embeddings in Many Languages</a>
	<li>Skim: <a href="https://arxiv.org/abs/2308.14963" target=_blank">Vector Search with OpenAI Embeddings: Lucene Is All You Need</a>

  </ul>
    </td>
</tr>

<tr><!--- Week 3 -->
  <td><strong>Week&nbsp;3</strong><br>(Jan&nbsp;22)</td>
  <td>LLMs I: Usage Patterns, Pre-training & Fine-Tuning
    </td>
  <td><ul>
<li>Pre-training
<li>Fine-tuning
<li>In-context learning
  </ul></td>
  <td><ul>
	<li>Read: <a href="http://jalammar.github.io/illustrated-transformer" target=_blank">The Illustrated Transformer</a>
	<li>Read: <a href="https://arxiv.org/pdf/1810.04805.pdf" target=_blank">BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding (focus on fine-tuning sections - tbd)</a>
	<li>Read: <a href="http://jalammar.github.io/how-gpt3-works-visualizations-animations/" target=_blank">How GPT-3 Works</a>
	<li>Skim:<a href="https://arxiv.org/pdf/2005.14165.pdf" target=_blank"> Language Models are Few-Shot Learners</a>
  </ul>
</tr>


<tr><!--- Week 4 -->
  <td><strong>Week&nbsp;4</strong><br>(Jan&nbsp;29)</td>
  <td>LLMs II: Reinforcement Learning & RLHF, and keeping LLMs on task
  <p><p>
  </td>
  <td><ul>
<li>Reinforcement Learning/RLHF
<li>Instruction-based Fine Tuning
<li>Alignment
  </ul></td>
  <td>
  <ul>
	<li>Read/Review: <a href="https://huggingface.co/tasks/reinforcement-learning" target=_blank">Reinforcement Learning</a> 
	<li>Read: <a href="https://proceedings.neurips.cc/paper_files/paper/2022/file/b1efde53be364a73914f58805a001731-Paper-Conference.pdf" target=_blank">Training Language Models to Follow Instructions with Human Feedback</a>
	<li>Read: <a href="https://arxiv.org/pdf/2209.00626.pdf" target=_blank">The Alignment Problem from a Deep Learning Perspective</a>
	<li>Skim: <a href="https://openreview.net/pdf?id=gEZrGCozdqR" target=_blank">Fine-tuned Language Models are Zero-Shot Learners</a>
	<li>Skim: <a href="https://openai.com/blog/our-approach-to-alignment-research" target=_blank">OpenAI's Alignment Approach</a>

</ul></td>
</tr>

<tr><!--- Week 5 -->
  <td><strong>Week&nbsp;5</strong><br>(Feb&nbsp;05)</td>
  <td>Context & Transformers: usages beyond NLP
  </td>
  <td><ul>
    <li>Encoder & Decoder architectures (high-levelish)
	<li>Pre-training in NLP (BERT & GPT)
	<li>Transformers for Vision & Audio, etc. 
	<li>Mixed models (CLIP, CLAP...)
	<li>Diffusion Models
  </ul></td>
  <td>
	<ul>
		<li>Read: <a href="https://machinelearningmastery.com/the-vision-transformer-model/" target=_blank">The Vision Transformer Model</a>
		<li>Read: <a href="http://proceedings.mlr.press/v139/radford21a/radford21a.pdf" target=_blank">Learning Transferable Visual Models From Natural Language Supervision</a>
		<li>Skim: <a href="https://arxiv.org/abs/2206.04769" target=_blank">CLAP : LEARNING AUDIO CONCEPTS FROM NATURAL LANGUAGE SUPERVISION</a>
		<li>Skim: <a href="https://aclanthology.org/2022.acl-long.421.pdf" target=_blank">CLIP Models are Few-shot Learners: Empirical Studies on VQA and Visual Entailment</a>
		<li>Skim: <a href="https://arxiv.org/pdf/2309.10020.pdf" target=_blank">Multimodel Foundation Models: From Specialists to General-Purpose Assistants</a>
  </ul>
  </td>
</tr>

<tr><td></td><td><strong>Part II: Practical Aspects & Techniques</strong></td><td></td><td></td></tr>

<tr><!--- Week 6 -->
  <td><strong>Week&nbsp;6</strong><br>(Feb&nbsp;12)</td>
  <td>Model & Training Efficiencies: Quantization, QLoRA, LoRA, Adapters and all that
  </td>
  <td><ul>
	<li>Distillation
	<li>LoRa
	<li>Quantization methods and QLoRa
	<li>Soft prompts & Adapters
  </ul></td>
  <td>
	<ul>
		<li>Read: <a href="https://huggingface.co/blog/hf-bitsandbytes-integration" target=_blank">A Gentle Introduction to 8-bit Matrix Multiplication for transformers at scale using Hugging Face Transformers, Accelerate and bitsandbytes</a>
		<li>Read: <a href="https://arxiv.org/abs/2106.09685" target=_blank">LoRA: LOW-RANK ADAPTATION OF LARGE LANGUAGE MODELS</a>
		<li>Skim: <a href="https://arxiv.org/abs/2305.14314" target=_blank">QLoRA: Efficient Finetuning of Quantized LLMs</a>
		<li>Skim: <a href="https://aclanthology.org/2021.emnlp-main.243" target=_blank">The Power of Scale for Parameter-Efficient Prompt Tuning</a>
		<li>Skim: <a href="https://aclanthology.org/2022.acl-long.346.pdf" target=_blank">SPoT: Better Frozen Model Adaptation through Soft Prompt Transfer</a>
		<li.>Skim: <a href="https://arxiv.org/pdf/2309.12307.pdf" target=_blank">LongLoRA: Efficient Fine-Tuning of Long-Contex Large Language Models</a>
		<li>Optional: <a href="https://blog.eleuther.ai/transformer-math/" target=_blank">Transformer Math 101</a>
  </ul>
  <p>
  </td>
</tr>

<tr><!--- Week 7  -->
  <td><strong>Week&nbsp;7</strong><br>(Feb&nbsp;19)</td>
  <td>Prompt Engineering
  </td>
  <td><ul>
	<li>Building prompt intuition
	<li>Basic prompt construction
	<li>Advanced prompt construction
	<li>Complex prompt structures
	<li>Automated prompt construction
  </ul></td>
  <td>
	<ul>
		<li>Read: <a href="https://arxiv.org/abs/2107.13586" target=_blank">Pre-train, Prompt, and Predict: A Systematic Survey of Prompting Methods in Natural Language Processing</a>
		<li>Read: <a href="https://hbr.org/2023/06/ai-prompt-engineering-isnt-the-future" target=_blank">AI Prompt Engineering Isn’t the Future</a>
		<li>Skim: <a href="https://openreview.net/pdf?id=_VjQlMeSB_J" target=_blank">Chain-of-Thought Prompting Elicits Reasoning in Large Language Models</a>
		<li>Skim: <a href="https://openreview.net/pdf?id=e2TBb5y0yFf" target=_blank">Large Language Models are Zero-Shot Reasoners</a>
		<li>Skim: <a href="https://learnprompting.org/docs/intro" target=_blank">Prompt Engineering Guide</a>
		<li>Optional: <a href="https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/" target=_blank">Prompt Engineering</a>
  </ul></td>
  </tr>
  


<tr><!--- Week 08  -->
  <td><strong>Week&nbsp;8</strong><br>(Feb&nbsp;26)</td>
  <td>Advanced Topics (context length, MoE, Grouped Attention)
  </td>
  <td><ul>
	<li>Techniques for extending context length
	<li>Strategies for using longer context
	<li>Mixture of Experts models
	<li>Grouped attention
  </ul></td>
  <td><ul>
	  <li>Read: <a href="https://medium.com/dair-ai/longformer-what-bert-should-have-been-78f4cd595be9" target=_blank">Longformer — The Long-Document Transformer</a>
	  <li>Read: <a href="https://www.anthropic.com/index/100k-context-windows" target=_blank">Anthropic’s 100K Context Window</a>
	  <li>Read: <a href="https://arxiv.org/abs/2307.03172" target=_blank">Lost in the Middle: How Language Models Use Long Context</a>
	  <li>Skim: <a href="https://arxiv.org/pdf/2310.03025.pdf" target=_blank">Retrieval Meets Long Context Large Language Models</a>
         <li>Skim: <a href="https://arxiv.org/pdf/2306.15595.pdf" target=_blank">Extending Context Window of Large Language Models Via Position Interpolation</a>
		 <li>Skim: <a href="https://huggingface.co/blog/moe" target=_blank">Hugging Face Blog: Mixture of Experts Explained</a>
  </ul>
  <p>
  </td>
</tr>

  <tr><!--- week 9  -->
  <td><strong>Week&nbsp;9</strong><br>(Mar&nbsp;04)</td>
  <td>MLOps & LLMOps - Putting LLMs into Production: Data, Training, Deployment, and Operational Considerations</td>
  <td><ul>
	<li>Hosted ecosystem: OpenAI, Cohere, Anthropic…
	<li>HuggingFace
	<li>GCP, AWS, Azure deployments
  </ul></td>
  <td><ul>
	<li>Read: <a href="https://wandb.ai/site/articles/what-is-mlops" target=_blank">MLOps: What It Is, And How To Implement The Right Solution (Weights & Biases)</a>
<li>Read: <a href="https://aws.amazon.com/what-is/mlops/" target=_blank">What is MLOps? (AWS)</a>
	<li>Read: <a href="https://cloud.google.com/vertex-ai/docs/pipelines/introduction" target=_blank">Introduction to Vertex AI Pipelines (GCP)</a>
	  <li>Skim: <a href="https://huggingface.co/blog/deploy-hugging-face-models-easily-with-amazon-sagemaker" target=_blank">Deploy Hugging Face models easily with Amazon SageMaker</a>
      <li>Skim: <a href="https://blog.vllm.ai/2023/06/20/vllm.html" target=_blank">vLLM: Easy, Fast, and Cheap LLM Serving with PagedAttention</a>
	      <li>Skim: <a href="https://blog.skypilot.co/serving-llm-24x-faster-on-the-cloud-with-vllm-and-skypilot/" target=_blank">Serving LLM 24x Faster On the Cloud with vLLM and SkyPilot</a>
	<li>Skim: <a href="https://eugeneyan.com/writing/llm-patterns/" target=_blank">Patterns for Building LLM-based Systems & Products</a>
  </ul>
  <p>
  </td>
</tr>

<tr><!--- Week 10  -->
  <td><strong>Week&nbsp;10</strong><br>(Mar&nbsp;11)</td>
  <td>Usage Patterns I: Retrieval-augmented Q&A and More</td>
  <td><ul>
	<li>Semantic Search
	<li>Retrieval Augmentation
	<li>LLama Index
	<li>Hallucination issues
  </ul></td>
  <td><ul>
<li>Read: <a href="https://research.ibm.com/blog/retrieval-augmented-generation-RAG" target=_blank">What is retrieval-augmented generation? </a>
<li>Read: <a href="https://lilianweng.github.io/posts/2020-10-29-odqa/#RAG" target=_blank">How to Build an Open-Domain Question Answering System</a>
<li>Read: <a href="https://proceedings.neurips.cc/paper/2020/file/6b493230205f780e1bc26945df7481e5-Paper.pdf" target=_blank">Retrieval Augmented Generation for Knowledge Intensive NLP Tasks</a>

  </ul>
  <p>
  </td>
</tr>


 <!-- <tr>
  <td><strong>Break</strong><br>(Nov&nbsp;6)</td>
  <td>No Async</td>
    <td>No class</td>
  <td>No Readings</td>
</tr>
-->

 <tr><!---   week 11 -->
  <td><strong>Week&nbsp;11</strong><br>(Mar&nbsp;18)</td>
  <td>Usage Patterns II: Chains & Agents</td>
  <td><ul>
	<li>Toolformer
	  <li>React
	<li>LangChain
        <li>Chains
	<li>Agents
 
		
  </ul></td>
  <td><ul>
	  <li>Read: <a href="https://python.langchain.com/docs/get_started/introduction" target=_blank">LangChain Documentation - Intro</a>
				<li>Read: <a href="https://www.pinecone.io/learn/series/langchain/langchain-agents/" target=_blank">Superpower LLMs with Conversational Agents</a>
					<li>Read: <a href="https://lilianweng.github.io/posts/2023-06-23-agent/" target=_blank">Lilian Weng Blog: LLM Powered Autonomous Agents</a>
	<li>Skim: <a href="https://arxiv.org/abs/2302.04761" target=_blank">Toolformer: Language Models Can Teach Themselves to Use Tools</a>
		<li>Skim: <a href="https://arxiv.org/abs/2210.03629" target=_blank">ReAct: Synergizing Reasoning and Acting in Large Language Models</a>
	<li>Skim: <a href="https://arxiv.org/abs/2203.06566" target=_blank">PromptChainer: Chaining Large Language Model Prompts through Visual Programming</a>
	<li>Skim: <a href="https://arxiv.org/abs/2305.15334" target=_blank">Gorilla: Large Language Model Connected with Massive APIs</a>
	
  </ul>
  <p>
  </td>
</tr>

<tr>
  <td><strong>Sping Break</strong><br>(Mar&nbsp;25)</td>
  <td>No Async</td>
    <td>No class</td>
  <td>No Readings</td>
</tr>

<tr><!--- Week 12  -->
  <td><strong>Week&nbsp;12</strong><br>(Apr&nbsp;01)</td>
  <td>Multi-modal Large Language Models: Text & Language, Images, and Sound</td>
  <td><ul>
	<li>Training of Image/Language Transformers
	<li>Text-to-image and image-to-text models
	<li>Sound to Text
	<li>Dual input models
	<li>Sound and Generative AI
  </ul>
  </td>
  <td><ul>
   <li>Read: <a href="http://jalammar.github.io/illustrated-stable-diffusion/" target=_blank">The Illustrated Stable Diffusion</a>
   <li>Read: <a href="https://arxiv.org/pdf/2309.11419" target=_blank">Kosmos-2.5 - A multimodal literate model</a>
   <li>Skim: <a href="https://arxiv.org/abs/2303.03378" target=_blank">Palm-E: An Embodied Multimodal Language Model</a>
   <li>Skim: <a href="https://arxiv.org/abs/2209.03143" target=_blank">AudioLM: a Language Modeling Approach to Audio Generation</a>
   <li>Optional: <a href="https://google-research.github.io/seanet/audiolm/examples/" target=_blank">AudioLM Demo</a>
   <li>Optional: <a href="https://arxiv.org/pdf/2212.04356.pdf" target=_blank">Robust Speech Recognition via Large-Scale Weak Supervision</a>
  </ul> 
  </td>
</tr>

<tr><td></td><td><strong>Part III: Challenges & Opportunities</strong></td><td></td><td></td></tr>

<tr><!--- Week 13  -->
  <td><strong>Week&nbsp;13</strong><br>(Apr&nbsp;08)</td>
  <td>Bias & Inclusivity, Safety, and Evaluation Approaches</td>
  <td><ul>
	<li>Safety metrics and evaluations
	<li>Bias questions
	<li>Faithfulness to facts vs making stuff up
	<li>Deep Fakes and their potential impact
  </ul></td>
  <td><ul>
	<li>Read: <a href="https://www.nytimes.com/2021/03/15/technology/artificial-intelligence-google-bias.html" target=_blank">Who Is Making Sure the A.I. Machines Aren’t Racist?</a>
<li>Read: <a href="https://arxiv.org/abs/2209.07858" target=_blank">Red Teaming Language Models to Reduce Harms: Methods, Scaling Behaviors, and Lessons Learned</a>
<li>Read: <a href="https://aclanthology.org/2022.emnlp-main.351" target=_blank">Should We Ban English NLP for a Year?</a>
<li>Skim: <a href="https://crfm.stanford.edu/helm/" target=_blank">Holistic Evaluation of Language Models</a>
  </ul>
  <p>
  </td>
</tr>


 <tr><!--- In class presentations week 14 -->
  <td><strong>Week&nbsp;14</strong><br>(Apr&nbsp;14)</td>
    <td>Some societal and legal considerations: Deep Fakes, usage rights, and IP questions, and the HUGE potential of LLMs & AI</td>
  <td><ul>
	<li>The fine-print in hosted models
	<li>The issue of hosted models learning from your data
	<li>IP questions around LLM... and their impact
	<li>The future of LLMs - a discussion
	<li>Data leakage
  </ul></td>
  <td><ul>
	<li>Revisit: <a href="https://arxiv.org/pdf/2307.10169.pdf" target=_blank">Challenges and Applications of Large Language Models</a>
<li>Read: <a href="https://www.theatlantic.com/technology/archive/2023/09/books3-database-meta-training-ai/675461/" target=_blank">My books were used to train Meta's Generative AI. Good.</a>
<li>Read: <a href="https://www.theatlantic.com/books/archive/2023/08/ai-chatbot-training-books-margaret-atwood/675151/" target=_blank">Murdered by my replica</a>
<li>Read: <a href="https://arstechnica.com/tech-policy/2023/05/lawyer-cited-6-fake-cases-made-up-by-chatgpt-judge-calls-it-unprecedented/" target=_blank">Lawyer cited 6 fake cases made up by ChatGPT; judge calls it “unprecedented”</a>
<li>Skim: <a href="https://arxiv.org/abs/2303.10130" target=_blank">GPTs are GPTs: An Early Look at the Labor Market Impact Potential of Large Language Models</a>
<li>Skim: <a href="https://www.anthropic.com/index/claudes-constitution" target=_blank">Claude's Constitution</a>
<li>Skim: <a href="https://arxiv.org/abs/2305.00118" target=_blank">Speak, Memory: An Archaeology of Books Known to ChatGPT/GPT-4</a>
  </ul>
  <p></td>
</tr>

</table>

Thanks for a great semester!
