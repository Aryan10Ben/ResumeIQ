
        document.addEventListener('DOMContentLoaded', () => {
            const dropZone = document.getElementById('dropZone');
            const fileInput = document.getElementById('resumeInput');
            const fileList = document.getElementById('fileList');
            const fileListWrapper = document.getElementById('fileListWrapper');
            const fileCountSpan = document.getElementById('fileCount');
            const btnClearFiles = document.getElementById('btnClearFiles');
            const jdTextarea = document.getElementById('jdTextarea');
            const charCountSpan = document.getElementById('charCount');
            const screenerForm = document.getElementById('screenerForm');
            const loadingOverlay = document.getElementById('loadingOverlay');

            // Drag and drop event listeners
            ['dragenter', 'dragover'].forEach(eventName => {
                dropZone.addEventListener(eventName, (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    dropZone.classList.add('dragover');
                }, false);
            });

            ['dragleave', 'drop'].forEach(eventName => {
                dropZone.addEventListener(eventName, (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    dropZone.classList.remove('dragover');
                }, false);
            });

            // Trigger file click when clicking browse button or drop zone
            dropZone.addEventListener('click', () => {
                fileInput.click();
            });

            // File selection change
            fileInput.addEventListener('change', handleFileSelection);

            // Handle drop event
            dropZone.addEventListener('drop', (e) => {
                const dt = e.dataTransfer;
                const files = dt.files;
                if (files.length > 0) {
                    fileInput.files = files;
                    handleFileSelection();
                }
            });

            // Populate selected files preview
            function handleFileSelection() {
                const files = fileInput.files;
                fileList.innerHTML = '';
                
                if (files.length > 0) {
                    fileListWrapper.style.display = 'block';
                    fileCountSpan.textContent = files.length;
                    
                    Array.from(files).forEach((file, index) => {
                        const li = document.createElement('li');
                        const isPDF = file.name.toLowerCase().endsWith('.pdf');
                        const fileIcon = isPDF ? 'fa-file-pdf pdf-color' : 'fa-file-lines txt-color';
                        
                        const left = document.createElement('div');
                        left.className = 'file-item-left';
                        const icon = document.createElement('i');
                        icon.className = 'fa-solid ' + fileIcon + ' file-item-icon';
                        const info = document.createElement('div');
                        info.className = 'file-item-info';
                        const label = document.createElement('span');
                        label.className = 'file-item-name';
                        label.title = file.name;
                        label.textContent = file.name;
                        const size = document.createElement('span');
                        size.className = 'file-item-size';
                        size.textContent = formatBytes(file.size);
                        const status = document.createElement('span');
                        status.className = 'file-item-status';
                        status.textContent = '✓ Ready';
                        info.append(label, size);
                        left.append(icon, info);
                        li.append(left, status);
                        fileList.appendChild(li);
                    });
                } else {
                    fileListWrapper.style.display = 'none';
                }
            }

            // Clear all files
            btnClearFiles.addEventListener('click', (e) => {
                e.stopPropagation();
                fileInput.value = '';
                handleFileSelection();
            });

            // Character counter for Job Description
            const MAX_LENGTH = 5000;
            const counterText = document.querySelector('.textarea-counter');
            
            jdTextarea.addEventListener('input', updateCharCounter);
            
            function updateCharCounter() {
                const len = jdTextarea.value.length;
                
                // Reset classes
                counterText.className = 'textarea-counter';
                
                if (len >= MAX_LENGTH) {
                    counterText.classList.add('limit-reached');
                } else if (len >= MAX_LENGTH * 0.9) {
                    counterText.classList.add('limit-warning');
                }
                
                counterText.textContent = `${len} / ${MAX_LENGTH}`;
            }

            // Show loading animation on submit
            screenerForm.addEventListener('submit', (e) => {
                if (fileInput.files.length === 0) {
                    alert("Please upload at least one resume.");
                    e.preventDefault();
                    return;
                }
                if (jdTextarea.value.trim() === '') {
                    alert("Please provide a job description.");
                    e.preventDefault();
                    return;
                }
                const selectedFiles = Array.from(fileInput.files);
                const totalBytes = selectedFiles.reduce((sum, file) => sum + file.size, 0);
                if (selectedFiles.length > 5 || selectedFiles.some(file => file.size > 3 * 1024 * 1024)
                    || totalBytes > 3.8 * 1024 * 1024) {
                    alert('Upload up to five resumes, maximum 3 MB each and 3.8 MB combined.');
                    e.preventDefault();
                    return;
                }
                loadingOverlay.classList.add('active');
            });

            // Format size string
            function formatBytes(bytes, decimals = 1) {
                if (bytes === 0) return '0 Bytes';
                const k = 1024;
                const dm = decimals < 0 ? 0 : decimals;
                const sizes = ['Bytes', 'KB', 'MB'];
                const i = Math.floor(Math.log(bytes) / Math.log(k));
                return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
            }
        });

        // Mock job description pre-loads for convenience
        function loadMockJD(type) {
            const jds = {
                ds: `Data Scientist Responsibilities:
- Design, train, and deploy Machine Learning models (supervised/unsupervised) to solve complex predictive problems.
- Extract, clean, and process large datasets using Python, Pandas, and NumPy.
- Build natural language processing (NLP) pipelines for classification and text sentiment.
- Work closely with cloud infrastructure on AWS (S3, SageMaker) to run model pipelines at scale.
- Present findings using data visualization tools like Matplotlib, Seaborn, or Tableau.
- Work within an Agile Scrum team environment.

Required Skills: Python, Machine Learning, NLP, Pandas, NumPy, Scikit-learn, AWS, SQL, Docker, Tableau.`,
                fs: `Full-Stack Web Developer Requirements:
- Build responsive and interactive user interfaces using React, HTML5, CSS3, and JavaScript/TypeScript.
- Design, build, and maintain RESTful API backends using Python and Flask.
- Integrate relational and non-relational database services such as PostgreSQL and MongoDB.
- Build secure, scalable applications utilizing Git version control, Docker containers, and CI/CD pipelines.
- Practice agile methodology (Scrum, Jira) to deliver clean, documented, and fully tested code.
- Knowledge of system design, Microservices, and cloud services (AWS or GCP).

Required Skills: Python, Flask, React, JavaScript, SQL, PostgreSQL, MongoDB, Git, Docker, Rest API.`,
                frontend: `Frontend Web Developer Responsibilities:
- Design and build responsive, highly interactive user interfaces using React, JavaScript, HTML5, and CSS3.
- Optimize client-side application performance and state management using Redux or TypeScript.
- Collaborate with UI/UX designers to translate Figma design mockups into pixel-perfect code.
- Write unit tests using Jest or Cypress and integrate with Git repositories.

Required Skills: React, JavaScript, TypeScript, HTML, CSS, Figma, Jest, Git, Redux.`,
                backend: `Backend Engineer Requirements:
- Build and maintain scalable, robust RESTful APIs using Python, Flask, Django, or Node.js.
- Design relational and non-relational database models with PostgreSQL, MySQL, and MongoDB.
- Implement security protocols, user authentication (OAuth, JWT), and secure API gateways.
- Collaborate with frontend engineers to integrate web applications and client services.

Required Skills: Python, Flask, Django, SQL, PostgreSQL, MongoDB, REST API, Node.js, Git, JWT.`,
                devops: `DevOps Engineer Requirements:
- Build, monitor, and automate deployment pipelines using CI/CD (Jenkins, GitHub Actions).
- Manage containerized systems and microservices using Docker and Kubernetes.
- Provision cloud infrastructure on AWS or GCP using Infrastructure as Code (Terraform).
- Write automation scripts using Bash, Python, or PowerShell in a Linux environment.

Required Skills: Docker, Kubernetes, AWS, GCP, Terraform, Git, Jenkins, Linux, Bash, CI/CD.`,
                mobile: `Mobile App Developer Responsibilities:
- Develop native mobile applications for iOS (Swift) and Android (Kotlin) or cross-platform applications using Flutter.
- Integrate mobile apps with RESTful backend APIs and cloud services.
- Optimize mobile performance, layout responsiveness, and offline database synchronization.
- Build, test, and release app builds to Apple App Store and Google Play Store.

Required Skills: Swift, Kotlin, Flutter, React Native, REST API, Git, Mobile, UI/UX.`,
                pm: `Product Manager Responsibilities:
- Define product vision, create product roadmap, and align engineering/design teams.
- Lead Agile Scrum teams, manage product backlog, and write user stories in Jira.
- Conduct user research, user surveys, and data analytics to optimize user journeys.
- Communicate product requirements and KPIs clearly to cross-functional stakeholders.

Required Skills: Project Management, Agile, Scrum, Jira, Communication, Leadership, Analytical Skills.`,
                uiux: `UI/UX & Product Designer Requirements:
- Create wireframes, user flows, and interactive high-fidelity prototypes in Figma or Sketch.
- Conduct usability testing, user research interviews, and user journey mapping.
- Establish and scale cohesive design systems and collaborate closely with frontend developers.
- Focus on typography, layout hierarchy, visual design, and user-centered solutions.

Required Skills: Figma, Sketch, Photoshop, Illustrator, UI/UX, Wireframing, Prototyping, User Research.`,
                qa: `QA Automation Engineer Requirements:
- Develop and execute automated test scripts for APIs and web frontends using Python, PyTest, or Selenium.
- Identify, document, and track software bugs and regressions in Jira.
- Integrate automated testing into CI/CD pipelines to ensure continuous delivery quality.
- Write detailed test cases, test plans, and collaborate with developers on code quality.

Required Skills: QA, Testing, PyTest, Selenium, Cypress, Python, Git, Jira, CI/CD.`,
                security: `Cybersecurity Analyst Responsibilities:
- Monitor network traffic, analyze security logs, and respond to potential security threats.
- Perform vulnerability assessments, penetration testing, and risk audits.
- Implement security firewalls, access controls (IAM), cryptography, and compliance benchmarks.
- Provide incident response guides and security training for engineering departments.

Required Skills: Cybersecurity, Cryptography, Linux, AWS, Network Security, Firewalls, Penetration Testing.`,
                data_eng: `Data Engineer Requirements:
- Build and optimize scalable ETL/ELT pipelines using Apache Airflow and Apache Spark.
- Design database warehouses and schemas using Snowflake, BigQuery, and SQL Server.
- Process big data streams using Apache Kafka and manage storage structures in Hadoop HDFS.
- Ensure data quality, logging, and metadata alignment across data repositories.

Required Skills: SQL, Python, Airflow, Spark, Kafka, Snowflake, BigQuery, Hadoop, Data Science.`,
                ml_eng: `Machine Learning Engineer Responsibilities:
- Build, train, optimize, and deploy Machine Learning and Deep Learning models (TensorFlow, PyTorch).
- Process unstructured data structures for Natural Language Processing (NLP) or Computer Vision models.
- Deploy models at scale as APIs using Flask, FastAPI, Docker, and AWS SageMaker.
- Build monitoring pipelines to track model drift, accuracy, and system latency.

Required Skills: Machine Learning, Deep Learning, Python, PyTorch, TensorFlow, Scikit-learn, NLP, Docker, AWS.`,
                cloud_arch: `Cloud Solutions Architect Requirements:
- Design high-availability, fault-tolerant, and cost-effective cloud architectures on AWS, GCP, or Azure.
- Configure cloud networks, VPCs, subnets, load balancing, and IAM configurations.
- Help transition legacy systems to modern Microservices and serverless infrastructure.
- Partner with DevOps engineers to configure auto-scaling group structures and logging.

Required Skills: AWS, GCP, Azure, Cloud Computing, Kubernetes, Terraform, System Design, Microservices.`,
                dba: `Database Administrator Responsibilities:
- Manage, monitor, configure, and tune database servers (PostgreSQL, MySQL, SQL Server, Oracle).
- Implement database high-availability structures, replicas, clustering, and backup recovery.
- Optimize database index systems and review slow queries to reduce database server latency.
- Ensure database security, user permission structures, and data encryption compliance.

Required Skills: SQL, PostgreSQL, MySQL, NoSQL, Oracle, Cassandra, SQLite, Linux, Backup.`,
                sys_admin: `Systems Administrator Responsibilities:
- Manage local and cloud servers running Linux (Ubuntu, CentOS) and Windows Server.
- Write automation scripts using Bash, PowerShell, or Python to manage backups and updates.
- Install, configure, and maintain network protocols, firewalls, and DNS systems.
- Monitor system hardware, CPU logs, disk storage, and manage user access policies.

Required Skills: Linux, Bash, PowerShell, Network Security, Firewalls, DNS, SSH, Active Directory.`,
                scrum: `Scrum Master / Agile Coach Responsibilities:
- Facilitate daily stand-ups, sprint planning, sprint retrospectives, and sprint backlog grooming.
- Support the Product Owner with product backlog management and scope validation.
- Identify and remove development blockers, shields, and organizational dependencies.
- Guide cross-functional teams toward agile maturity, self-organization, and high performance.

Required Skills: Scrum, Agile, Jira, Confluence, Project Management, Communication, Leadership.`,
                embedded: `Embedded Systems Engineer Requirements:
- Design and write firmware and drivers for microcontrollers using C and C++ programming.
- Interface with hardware peripherals and sensors using communication protocols (SPI, I2C, UART).
- Work with Real-Time Operating Systems (RTOS) and debug code using oscilloscopes and logic analyzers.
- Optimize firmware memory, power consumption, and hardware execution cycles.

Required Skills: C++, C, Linux, Git, Microcontrollers, RTOS, Hardware, Embedded.`,
                blockchain: `Blockchain Developer Responsibilities:
- Design and implement decentralized applications (DApps) and smart contracts in Solidity or Rust.
- Build Web3 integrations and connect frontends with blockchain networks (Ethereum, Solana).
- Write test scripts for smart contracts and audit them for security vulnerabilities.
- Configure decentralized file storage networks (IPFS) and crypto payment channels.

Required Skills: Blockchain, Solidity, Rust, Cryptography, Web3, Git, Ethereum, Smart Contracts.`,
                tech_writer: `Technical Writer Responsibilities:
- Write and maintain clear developer documentation, API guides, user manuals, and tutorials.
- Review codebase code styles and write inline docstrings and Markdown reference templates.
- Partner with product managers and engineers to document system features and product release notes.
- Organize documentation portals and manage formatting, markup structures, and searchability.

Required Skills: Technical Writing, Markdown, Git, Communication, Word, Google Docs, HTML.`,
                sre: `Site Reliability Engineer Requirements:
- Optimize system availability, scalability, and performance of cloud applications.
- Design and measure Service Level Indicators (SLIs) and Service Level Objectives (SLOs).
- Implement telemetry, logging, monitoring systems (Prometheus, Grafana, ELK Stack).
- Build automated scripting to manage system failovers and lead incident post-mortem reviews.

Required Skills: DevOps, SRE, Prometheus, Grafana, Linux, Kubernetes, AWS, Bash, Python, Docker.`
            };
            
            if (jds[type]) {
                const textarea = document.getElementById('jdTextarea');
                textarea.value = jds[type];
                // Trigger input event to update char counter
                const event = new Event('input', { bubbles: true });
                textarea.dispatchEvent(event);
            }
        }
    