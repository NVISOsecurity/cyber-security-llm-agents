# cyber-security-llm-agents
A collection of agents that use Large Language Models (LLMs) to perform tasks common on our day to day jobs in cyber security.
Built on top of [AutoGen](https://microsoft.github.io/autogen/).

<figure align="center">
  <img src="documentation/videos/detect_edr.gif" alt="Detecting EDR"/>
  <figcaption>Dynamically detecting the EDR running on a Windows system. Extracts a list of Security Products mentioned in https://github.com/tsale/EDR-Telemetry and compares it with the names of running services on the endpoint.</figcaption>
</figure>

## Key Features

- **Modular Design**: Our framework is composed of individual agents and tasks that can be combined and customized to fit your specific security needs. This modular approach ensures flexibility and scalability, allowing you to adapt to the ever-evolving landscape of cyber threats.
- **Automation**: With Cyber-Security-LLM-Agents, you can automate repetitive and complex tasks, freeing up valuable time for your security team to focus on strategic analysis and decision-making.
- **Batteries Included**: We provide a comprehensive set of pre-defined workflows, agents, and tasks that are ready to use out-of-the-box. This enables you to jumpstart your cyber security automation with proven practices and techniques.


## Getting Started

### Step 1 - Install  requirements

```
pip install -r requirements
```

### Step 2 - Configure OpenAI API Information

```
cp .env_template .env
```
Then add your LLM API information and other parameters to the ``.env``.

### Step 3 - Start HTTP and FTP server (Optional)

Only required if you want to host a simple HTTP and FTP server to interact with using your agents.
This is useful for demos, where you might want to showcase exfiltration or downloading of information.

```
python run_servers.py
```

### Step 4 - Run Jupyter notebook (Optional)

You can launch jupyter notebooks on your network interface by choice.
This allows you run the notebooks within a VM and expose them to different system - again, interesting for demos!

```
./run_notebooks.sh ens37
```
## Development

### Static analysis (code quality)

We ignore E501 (line too long) as this triggers on long agent and action strings.
We ignore W503 (line break before binary operator) as we are opinionated about this being OK.

```
flake8 --exclude=.venv --ignore=E501,W503 .
```

## Contribution

We welcome contributions from the community! 
If you have ideas for new agents, tasks, or improvements, please feel free to fork our repository, make your changes, and submit a pull request.

## Contact Us

For any questions or support, please open an issue in our GitHub repository, and our team will be happy to assist.
