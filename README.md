<html>
	<body>
		<h1>Hey there , I am Rachel !</h1>
		<br>
		<p>Hi , I am an assistant written in <b>Python !</b></p>
		<p>I can't do many difficult stuff , but I am a <b>lovely</b> Assistant !</p>
		<p>It's required to have <b>MySQL</b> on your device .</p>
		<p>The are some Python Modules you need to install . You can see them <a href="https://github.com/BlackIQ/Rachel/blob/master/req.txt">Here</a> .</p>
		<p>There are some steps before running !</p>
		<ul>
		    <li><a href="https://github.com/BlackIQ/Rachel#packages-need-to-be-install-debian-">Install packages</a></li>
		    <li><a href="https://github.com/BlackIQ/Rachel#mysql-configuration-">Configure MySQL</a></li>
		    <li><a href="https://github.com/BlackIQ/Rachel#how-to-run-">Clone & install requirements & Run Rachel</a></li>
		</ul>
		<hr>
		<h3>Packages need to be install (debian) :</h3>
		<code>
		    $ sudo apt install mysql-server mysql-client espeak ffmpeg python3-pip
        </code>
		<br>
        <code>
            $ sudo systemctl restart mysql.service
        </code>
        <br>
        <br>
        <b>There are the all package you need , try dnf install on fedora , pacman -S on Arch bases , eopkg it on Solus and ETC .</b>
		<hr>
		<h3>MySQL Configuration :</h3>
		<code>
		    $ sudo mysql
		</code>
		<br>
		<code>
		    > CREATE USER 'Rachel'@'localhost' IDENTIFIED BY 'Rachel';
		</code>
		<br>
		<code>
		    > GRANT ALL PRIVILEGES ON *.* TO 'newuser'@'localhost';
        </code>
        <br>
        <code>
            > FLUSH PRIVILEGES;
        </code>
        <br>
        <code>
            > exit
        </code>
        <br>
        <code>
            $ sudo systemctl restart mysql.service
        </code>
		<hr>
		<h3>How To Run :</h3>
		<code>
		    $ git clone https://github.com/BlackIQ/Rachel && cd Rachel
		</code>
		<br>
		<code>
		    $ python3 -m venv venv && source venv/bin/activate
		</code>
		<br>
		<code>
		    $ pip3 install -r req.txt && alias Rachel="python3 Rachel.py"
		</code>
		<br>
		<code>
		    $ python3 setup.py
		</code>
		<br>
		<code>
		    $ Rachel
		</code>
		<hr>
		<p>There is just a person who had contributed on me !</p>
		<p>Many thanks from <b><a href="https://github.com/erfansaberi">Erfan Saberi</a></b> &hearts; !</p>
		<p>Contribute on me !</p>
	</body>
</html>