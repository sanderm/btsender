<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="generator" content="Docutils 0.3.7: http://docutils.sourceforge.net/" />
<title>BTSender 1.1.0</title>
<meta name="author" content="Arve Barsnes/Sander Johansen" />
<link rel="stylesheet" href="default.css" type="text/css" />
</head>
<body>
<div class="document" id="btsender-1-1-0">
<h1 class="title"><a class="reference" href="http://folk.uio.no/sanderj/btsender/">BTSender</a> 1.1.0</h1>
<table class="docinfo" frame="void" rules="none">
<col class="docinfo-name" />
<col class="docinfo-content" />
<tbody valign="top">
<tr><th class="docinfo-name">Author:</th>
<td>Arve Barsnes/Sander Johansen</td></tr>
<tr><th class="docinfo-name">Contact:</th>
<td><a class="first last reference" href="mailto:arveba/sanderj&#64;ifi.uio.no">arveba/sanderj&#64;ifi.uio.no</a></td></tr>
</tbody>
</table>
<div class="contents topic" id="contents">
<p class="topic-title first"><a name="contents">Contents</a></p>
<ul class="auto-toc simple">
<li><a class="reference" href="#introduction" id="id1" name="id1">1&nbsp;&nbsp;&nbsp;Introduction</a></li>
<li><a class="reference" href="#compatibility" id="id2" name="id2">2&nbsp;&nbsp;&nbsp;Compatibility</a></li>
<li><a class="reference" href="#installation" id="id3" name="id3">3&nbsp;&nbsp;&nbsp;Installation</a></li>
<li><a class="reference" href="#implementation-notes" id="id4" name="id4">4&nbsp;&nbsp;&nbsp;Implementation notes</a></li>
<li><a class="reference" href="#sample-usage" id="id5" name="id5">5&nbsp;&nbsp;&nbsp;Sample usage</a></li>
<li><a class="reference" href="#test-suite" id="id6" name="id6">6&nbsp;&nbsp;&nbsp;Test suite</a></li>
<li><a class="reference" href="#documentation-generation" id="id7" name="id7">7&nbsp;&nbsp;&nbsp;Documentation generation</a></li>
<li><a class="reference" href="#download" id="id8" name="id8">8&nbsp;&nbsp;&nbsp;Download</a></li>
<li><a class="reference" href="#licence" id="id9" name="id9">9&nbsp;&nbsp;&nbsp;Licence</a></li>
<li><a class="reference" href="#references" id="id10" name="id10">10&nbsp;&nbsp;&nbsp;References</a></li>
</ul>
</div>
<div class="section" id="introduction">
<h1><a class="toc-backref" href="#id1" name="introduction">1&nbsp;&nbsp;&nbsp;Introduction</a></h1>
<p>BTSender is a package that will act as an automatic file pusher
that sends a list of files to any detectable BlueTooth devices in
the vicinity.</p>
</div>
<div class="section" id="compatibility">
<h1><a class="toc-backref" href="#id2" name="compatibility">2&nbsp;&nbsp;&nbsp;Compatibility</a></h1>
<p>There are three required libraries to use this package, BlueZ [bluez],
PyBlueZ [pybluez] and openobex [openobex].</p>
</div>
<div class="section" id="installation">
<h1><a class="toc-backref" href="#id3" name="installation">3&nbsp;&nbsp;&nbsp;Installation</a></h1>
<p>Unpack the file. This is typically accomplished by running:</p>
<pre class="literal-block">
$ tar -xzf &lt;archive-name&gt;
</pre>
<p>Enter the generated directory, and then run this:</p>
<pre class="literal-block">
$ python setup.py install
</pre>
<p>The package will be installed to ~/BTSender</p>
</div>
<div class="section" id="implementation-notes">
<h1><a class="toc-backref" href="#id4" name="implementation-notes">4&nbsp;&nbsp;&nbsp;Implementation notes</a></h1>
<p>The shell around the core sending functions is implemented in
Python, while the actual sending, which uses the obex protocol, is
mostly ripped directly from ussp-push [ussp-push], only slightly
rewritten to allow it to be called directly from within python, and
other small changes to accomodate the wanted functionality.</p>
</div>
<div class="section" id="sample-usage">
<h1><a class="toc-backref" href="#id5" name="sample-usage">5&nbsp;&nbsp;&nbsp;Sample usage</a></h1>
<p>The package is easy to use. All you have to do is go to the
installation-directory (~/BTSender). There you type:</p>
<pre class="literal-block">
$ ./start.sh
</pre>
<p>This will setup an important environment variable so the program
will find the libraries, and start BTSender.</p>
<p>Once running, it will search for any nearby BlueTooth devices and
send them the files. Any files in the files subdirectory will be
pushed out, so if there are files in there you don't want to send
they will have to be deleted or moved out. Likewise, if there are
new files you want to push out, put them in this directory, and
all detected devices will get this file as well.</p>
</div>
<div class="section" id="test-suite">
<h1><a class="toc-backref" href="#id6" name="test-suite">6&nbsp;&nbsp;&nbsp;Test suite</a></h1>
<p>Running the unit tests should be a simple matter of running:</p>
<pre class="literal-block">
$ python unittests.py
</pre>
<p>Although, if you haven't already run the program beforehand, you
should setup the variable that the start.sh script does. To do
this manually, simply type:</p>
<pre class="literal-block">
$ export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
</pre>
</div>
<div class="section" id="documentation-generation">
<h1><a class="toc-backref" href="#id7" name="documentation-generation">7&nbsp;&nbsp;&nbsp;Documentation generation</a></h1>
<p>An HTML version of the documentation in this file may be produced
using docutils, like this:</p>
<pre class="literal-block">
$ rst2html README &gt;README.html
</pre>
<p>or a LaTeX version like this:</p>
<pre class="literal-block">
$ rst2latex README &gt;README.tex
</pre>
</div>
<div class="section" id="download">
<h1><a class="toc-backref" href="#id8" name="download">8&nbsp;&nbsp;&nbsp;Download</a></h1>
<p>The latest version of this library should be available at
<a class="reference" href="http://folk.uio.no/sanderj/btsender/BTSender-latest.tar.gz">http://folk.uio.no/sanderj/btsender/BTSender-latest.tar.gz</a></p>
</div>
<div class="section" id="licence">
<h1><a class="toc-backref" href="#id9" name="licence">9&nbsp;&nbsp;&nbsp;Licence</a></h1>
<p>BTSender by Arve and Sander ( Bluetooth Sender )
Copyright (C) 2006  Arve Barsnes and Sander Johansen</p>
<p>This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.</p>
<p>This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.</p>
<p>You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA</p>
<p>Sander Johansen &lt;<a class="reference" href="mailto:sanderj&#64;ifi.uio.no">sanderj&#64;ifi.uio.no</a>&gt;
Arve Barsnes &lt;<a class="reference" href="mailto:arveba&#64;ifi.uio.no">arveba&#64;ifi.uio.no</a>&gt;</p>
</div>
<div class="section" id="references">
<h1><a class="toc-backref" href="#id10" name="references">10&nbsp;&nbsp;&nbsp;References</a></h1>
<table class="docutils citation" frame="void" id="bluez" rules="none">
<colgroup><col class="label" /><col /></colgroup>
<tbody valign="top">
<tr><td class="label"><a name="bluez">[bluez]</a></td><td><a class="reference" href="http://www.bluez.org/">http://www.bluez.org/</a></td></tr>
</tbody>
</table>
<table class="docutils citation" frame="void" id="pybluez" rules="none">
<colgroup><col class="label" /><col /></colgroup>
<tbody valign="top">
<tr><td class="label"><a name="pybluez">[pybluez]</a></td><td><a class="reference" href="http://org.csail.mit.edu/pybluez/">http://org.csail.mit.edu/pybluez/</a></td></tr>
</tbody>
</table>
<table class="docutils citation" frame="void" id="openobex" rules="none">
<colgroup><col class="label" /><col /></colgroup>
<tbody valign="top">
<tr><td class="label"><a name="openobex">[openobex]</a></td><td><a class="reference" href="http://openobex.triq.net/">http://openobex.triq.net/</a></td></tr>
</tbody>
</table>
<table class="docutils citation" frame="void" id="ussp-push" rules="none">
<colgroup><col class="label" /><col /></colgroup>
<tbody valign="top">
<tr><td class="label"><a name="ussp-push">[ussp-push]</a></td><td><a class="reference" href="http://www.xmailserver.org/ussp-push.html">http://www.xmailserver.org/ussp-push.html</a></td></tr>
</tbody>
</table>
<!-- Local Variables:
mode: indented-text
indent-tabs-mode: nil
sentence-end-double-space: t
fill-column: 70
End: -->
</div>
</div>
</body>
</html>
