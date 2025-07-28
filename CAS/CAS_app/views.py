from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import NewsletterForm
from .models import NewsletterSubscriber
from django.core.files.storage import default_storage
import pandas as pd
import fitz
import re
from sentence_transformers import SentenceTransformer, util
import os
from django.conf import settings

# Create your views here.

def home_view(request):
    return render(request, "website/home.html")


#----------- Resume Advisor View -----------

# === Skill Keywords ===
skills_keywords = [
    {"Skill": "Python Programming", "Category": "Programming Languages"},
    {"Skill": "Java Programming", "Category": "Programming Languages"},
    {"Skill": "JavaScript Programming", "Category": "Programming Languages"},
    {"Skill": "C++ Programming", "Category": "Programming Languages"},
    {"Skill": "C# Programming", "Category": "Programming Languages"},
    {"Skill": "Go Programming", "Category": "Programming Languages"},
    {"Skill": "Rust Programming", "Category": "Programming Languages"},
    {"Skill": "Ruby Programming", "Category": "Programming Languages"},
    {"Skill": "PHP Programming", "Category": "Programming Languages"},
    {"Skill": "Swift Programming", "Category": "Programming Languages"},
    {"Skill": "Kotlin Programming", "Category": "Programming Languages"},
    {"Skill": "TypeScript Programming", "Category": "Programming Languages"},
    {"Skill": "SQL Programming", "Category": "Programming Languages"},
    {"Skill": "R Programming", "Category": "Programming Languages"},
    {"Skill": "Dart Programming", "Category": "Programming Languages"},
    {"Skill": "Assembly Language", "Category": "Programming Languages"},
    {"Skill": "Scala Programming", "Category": "Programming Languages"},
    {"Skill": "Solidity Programming", "Category": "Programming Languages"},
    {"Skill": "Vyper Programming", "Category": "Programming Languages"},
    {"Skill": "Ada Programming", "Category": "Programming Languages"},
    {"Skill": "Fortran Programming", "Category": "Programming Languages"},
    {"Skill": "Bash Scripting", "Category": "Scripting"},
    {"Skill": "PowerShell Scripting", "Category": "Scripting"},
    {"Skill": "HTML", "Category": "Web Development"},
    {"Skill": "CSS", "Category": "Web Development"},
    {"Skill": "React Framework", "Category": "Frontend Frameworks"},
    {"Skill": "Angular Framework", "Category": "Frontend Frameworks"},
    {"Skill": "Vue.js Framework", "Category": "Frontend Frameworks"},
    {"Skill": "Svelte Framework", "Category": "Frontend Frameworks"},
    {"Skill": "Node.js Framework", "Category": "Backend Frameworks"},
    {"Skill": "Express Framework", "Category": "Backend Frameworks"},
    {"Skill": "Django Framework", "Category": "Backend Frameworks"},
    {"Skill": "Spring Boot Framework", "Category": "Backend Frameworks"},
    {"Skill": "Flask Framework", "Category": "Backend Frameworks"},
    {"Skill": "Ruby on Rails Framework", "Category": "Backend Frameworks"},
    {"Skill": "Laravel Framework", "Category": "Backend Frameworks"},
    {"Skill": ".NET Framework", "Category": "Backend Frameworks"},
    {"Skill": "ASP.NET Framework", "Category": "Backend Frameworks"},
    {"Skill": "Hibernate Framework", "Category": "Backend Frameworks"},
    {"Skill": "MySQL Database", "Category": "Databases"},
    {"Skill": "PostgreSQL Database", "Category": "Databases"},
    {"Skill": "MongoDB Database", "Category": "Databases"},
    {"Skill": "DynamoDB Database", "Category": "Databases"},
    {"Skill": "Oracle Database", "Category": "Databases"},
    {"Skill": "SQL Server Database", "Category": "Databases"},
    {"Skill": "Redis Database", "Category": "Databases"},
    {"Skill": "Cassandra Database", "Category": "Databases"},
    {"Skill": "Snowflake Database", "Category": "Databases"},
    {"Skill": "HBase Database", "Category": "Databases"},
    {"Skill": "PostGIS Database", "Category": "Databases"},
    {"Skill": "REST API Development", "Category": "API Development"},
    {"Skill": "GraphQL API Development", "Category": "API Development"},
    {"Skill": "gRPC API Development", "Category": "API Development"},
    {"Skill": "SOAP API Development", "Category": "API Development"},
    {"Skill": "API Authentication (OAuth, JWT)", "Category": "API Development"},
    {"Skill": "AWS Cloud Platform", "Category": "Cloud Platforms"},
    {"Skill": "Azure Cloud Platform", "Category": "Cloud Platforms"},
    {"Skill": "Google Cloud Platform", "Category": "Cloud Platforms"},
    {"Skill": "AWS Lambda", "Category": "Cloud Services"},
    {"Skill": "Azure Functions", "Category": "Cloud Services"},
    {"Skill": "Google Cloud Functions", "Category": "Cloud Services"},
    {"Skill": "AWS EC2", "Category": "Cloud Services"},
    {"Skill": "AWS S3", "Category": "Cloud Services"},
    {"Skill": "AWS RDS", "Category": "Cloud Services"},
    {"Skill": "Azure Cosmos DB", "Category": "Cloud Services"},
    {"Skill": "Google BigQuery", "Category": "Cloud Services"},
    {"Skill": "Docker Containerization", "Category": "DevOps"},
    {"Skill": "Kubernetes Orchestration", "Category": "DevOps"},
    {"Skill": "Jenkins CI/CD", "Category": "DevOps"},
    {"Skill": "GitLab CI/CD", "Category": "DevOps"},
    {"Skill": "CircleCI CI/CD", "Category": "DevOps"},
    {"Skill": "Terraform Infrastructure as Code", "Category": "DevOps"},
    {"Skill": "Ansible Automation", "Category": "DevOps"},
    {"Skill": "Puppet Automation", "Category": "DevOps"},
    {"Skill": "CloudFormation IaC", "Category": "DevOps"},
    {"Skill": "Git Version Control", "Category": "Version Control"},
    {"Skill": "GitHub", "Category": "Version Control"},
    {"Skill": "GitLab", "Category": "Version Control"},
    {"Skill": "Bitbucket", "Category": "Version Control"},
    {"Skill": "Perforce", "Category": "Version Control"},
    {"Skill": "TensorFlow Framework", "Category": "Machine Learning"},
    {"Skill": "PyTorch Framework", "Category": "Machine Learning"},
    {"Skill": "Scikit-learn Library", "Category": "Machine Learning"},
    {"Skill": "Keras Library", "Category": "Machine Learning"},
    {"Skill": "Hugging Face Transformers", "Category": "Machine Learning"},
    {"Skill": "OpenAI Gym", "Category": "Machine Learning"},
    {"Skill": "Stable Baselines", "Category": "Machine Learning"},
    {"Skill": "XGBoost Library", "Category": "Machine Learning"},
    {"Skill": "MLflow MLOps", "Category": "MLOps"},
    {"Skill": "Kubeflow MLOps", "Category": "MLOps"},
    {"Skill": "TFX (TensorFlow Extended)", "Category": "MLOps"},
    {"Skill": "OpenCV Library", "Category": "Computer Vision"},
    {"Skill": "YOLO Framework", "Category": "Computer Vision"},
    {"Skill": "OpenPose Library", "Category": "Computer Vision"},
    {"Skill": "NLTK Library", "Category": "Natural Language Processing"},
    {"Skill": "SpaCy Library", "Category": "Natural Language Processing"},
    {"Skill": "BERT Model", "Category": "Natural Language Processing"},
    {"Skill": "GPT Model", "Category": "Natural Language Processing"},
    {"Skill": "Unity Game Engine", "Category": "Game Development"},
    {"Skill": "Unreal Engine", "Category": "Game Development"},
    {"Skill": "Godot Engine", "Category": "Game Development"},
    {"Skill": "OpenGL Graphics API", "Category": "Graphics Programming"},
    {"Skill": "DirectX Graphics API", "Category": "Graphics Programming"},
    {"Skill": "Vulkan Graphics API", "Category": "Graphics Programming"},
    {"Skill": "GLSL Shader Language", "Category": "Graphics Programming"},
    {"Skill": "HLSL Shader Language", "Category": "Graphics Programming"},
    {"Skill": "CUDA GPU Programming", "Category": "High-Performance Computing"},
    {"Skill": "OpenCL GPU Programming", "Category": "High-Performance Computing"},
    {"Skill": "MPI Parallel Programming", "Category": "High-Performance Computing"},
    {"Skill": "OpenMP Parallel Programming", "Category": "High-Performance Computing"},
    {"Skill": "Apache Kafka Streaming", "Category": "Streaming Systems"},
    {"Skill": "Apache Flink Streaming", "Category": "Streaming Systems"},
    {"Skill": "Spark Streaming", "Category": "Streaming Systems"},
    {"Skill": "RabbitMQ Messaging", "Category": "Messaging Systems"},
    {"Skill": "ActiveMQ Messaging", "Category": "Messaging Systems"},
    {"Skill": "MQTT Protocol", "Category": "IoT"},
    {"Skill": "CoAP Protocol", "Category": "IoT"},
    {"Skill": "ROS (Robot Operating System)", "Category": "Robotics"},
    {"Skill": "ROS2", "Category": "Robotics"},
    {"Skill": "Qiskit Quantum Framework", "Category": "Quantum Computing"},
    {"Skill": "Cirq Quantum Framework", "Category": "Quantum Computing"},
    {"Skill": "PennyLane Quantum Framework", "Category": "Quantum Computing"},
    {"Skill": "Biopython Library", "Category": "Bioinformatics"},
    {"Skill": "BLAST Tool", "Category": "Bioinformatics"},
    {"Skill": "SAMtools", "Category": "Bioinformatics"},
    {"Skill": "ArcGIS Platform", "Category": "Geographic Information Systems"},
    {"Skill": "QGIS Platform", "Category": "Geographic Information Systems"},
    {"Skill": "Leaflet Library", "Category": "Geographic Information Systems"},
    {"Skill": "D3.js Visualization", "Category": "Data Visualization"},
    {"Skill": "Chart.js Visualization", "Category": "Data Visualization"},
    {"Skill": "Tableau Visualization", "Category": "Data Visualization"},
    {"Skill": "Power BI Visualization", "Category": "Data Visualization"},
    {"Skill": "Hadoop Big Data", "Category": "Big Data"},
    {"Skill": "Apache Spark Big Data", "Category": "Big Data"},
    {"Skill": "Airflow ETL", "Category": "ETL"},
    {"Skill": "Informatica ETL", "Category": "ETL"},
    {"Skill": "Talend ETL", "Category": "ETL"},
    {"Skill": "Salesforce CRM Development", "Category": "CRM/ERP"},
    {"Skill": "Microsoft Dynamics 365", "Category": "CRM/ERP"},
    {"Skill": "SAP ERP Development", "Category": "CRM/ERP"},
    {"Skill": "NetSuite ERP Development", "Category": "CRM/ERP"},
    {"Skill": "Apex Programming", "Category": "CRM/ERP"},
    {"Skill": "ABAP Programming", "Category": "CRM/ERP"},
    {"Skill": "Shopify Platform", "Category": "E-Commerce"},
    {"Skill": "Magento Platform", "Category": "E-Commerce"},
    {"Skill": "WooCommerce Platform", "Category": "E-Commerce"},
    {"Skill": "Ethereum Blockchain", "Category": "Blockchain"},
    {"Skill": "Hyperledger Blockchain", "Category": "Blockchain"},
    {"Skill": "Binance Smart Chain", "Category": "Blockchain"},
    {"Skill": "Truffle Blockchain Tool", "Category": "Blockchain"},
    {"Skill": "Hardhat Blockchain Tool", "Category": "Blockchain"},
    {"Skill": "OpenSSL Cryptography", "Category": "Cryptography"},
    {"Skill": "Crypto++ Library", "Category": "Cryptography"},
    {"Skill": "Libsodium Library", "Category": "Cryptography"},
    {"Skill": "Metasploit Penetration Testing", "Category": "Cybersecurity"},
    {"Skill": "Burp Suite Security", "Category": "Cybersecurity"},
    {"Skill": "Nessus Vulnerability Scanning", "Category": "Cybersecurity"},
    {"Skill": "Splunk Security Monitoring", "Category": "Cybersecurity"},
    {"Skill": "Wireshark Network Analysis", "Category": "Cybersecurity"},
    {"Skill": "OWASP Security Standards", "Category": "Cybersecurity"},
    {"Skill": "NIST Cybersecurity Framework", "Category": "Cybersecurity"},
    {"Skill": "ISO 27001 Compliance", "Category": "Cybersecurity"},
    {"Skill": "PCI DSS Compliance", "Category": "Compliance"},
    {"Skill": "GDPR Compliance", "Category": "Compliance"},
    {"Skill": "HIPAA Compliance", "Category": "Compliance"},
    {"Skill": "FHIR Healthcare Standard", "Category": "Healthcare Standards"},
    {"Skill": "HL7 Healthcare Standard", "Category": "Healthcare Standards"},
    {"Skill": "CAN Automotive Protocol", "Category": "Automotive Protocols"},
    {"Skill": "LIN Automotive Protocol", "Category": "Automotive Protocols"},
    {"Skill": "Modbus Industrial Protocol", "Category": "Industrial Protocols"},
    {"Skill": "OPC UA Industrial Protocol", "Category": "Industrial Protocols"},
    {"Skill": "DO-178C Aerospace Standard", "Category": "Aerospace Standards"},
    {"Skill": "ISO 26262 Automotive Standard", "Category": "Automotive Standards"},
    {"Skill": "Sass CSS Preprocessor", "Category": "Web Development"},
    {"Skill": "LESS CSS Preprocessor", "Category": "Web Development"},
    {"Skill": "Tailwind CSS Framework", "Category": "Web Development"},
    {"Skill": "Bootstrap Framework", "Category": "Web Development"},
    {"Skill": "Webpack Build Tool", "Category": "Build Tools"},
    {"Skill": "Vite Build Tool", "Category": "Build Tools"},
    {"Skill": "Postman API Testing", "Category": "API Tools"},
    {"Skill": "Swagger API Documentation", "Category": "API Tools"},
    {"Skill": "Selenium Testing", "Category": "Testing"},
    {"Skill": "JUnit Testing", "Category": "Testing"},
    {"Skill": "TestNG Testing", "Category": "Testing"},
    {"Skill": "Cypress Testing", "Category": "Testing"},
    {"Skill": "JMeter Performance Testing", "Category": "Performance Testing"},
    {"Skill": "LoadRunner Performance Testing", "Category": "Performance Testing"},
    {"Skill": "Prometheus Monitoring", "Category": "Monitoring"},
    {"Skill": "Grafana Monitoring", "Category": "Monitoring"},
    {"Skill": "Nagios Monitoring", "Category": "Monitoring"},
    {"Skill": "New Relic Monitoring", "Category": "Monitoring"},
    {"Skill": "MATLAB Simulation", "Category": "Simulation"},
    {"Skill": "Simulink Simulation", "Category": "Simulation"},
    {"Skill": "Gazebo Simulation", "Category": "Simulation"},
    {"Skill": "Agile Methodologies", "Category": "Methodologies"},
    {"Skill": "Scrum Framework", "Category": "Methodologies"},
    {"Skill": "Kanban Methodology", "Category": "Methodologies"},
    {"Skill": "DevOps Practices", "Category": "Methodologies"},
    {"Skill": "DevSecOps Practices", "Category": "Methodologies"},
    {"Skill": "Microservices Architecture", "Category": "System Architecture"},
    {"Skill": "Service-Oriented Architecture (SOA)", "Category": "System Architecture"},
    {"Skill": "TOGAF Architecture Framework", "Category": "System Architecture"},
    {"Skill": "Problem-Solving Skills", "Category": "Soft Skills"},
    {"Skill": "Team Collaboration", "Category": "Soft Skills"},
    {"Skill": "Communication Skills", "Category": "Soft Skills"},
    {"Skill": "Analytical Thinking", "Category": "Soft Skills"},
    {"Skill": "Time Management", "Category": "Soft Skills"},
    {"Skill": "Leadership Skills", "Category": "Soft Skills"},
    {"Skill": "Attention to Detail", "Category": "Soft Skills"},
    {"Skill": "Code Review Practices", "Category": "Development Practices"},
    {"Skill": "Unit Testing", "Category": "Development Practices"},
    {"Skill": "Test-Driven Development (TDD)", "Category": "Development Practices"},
    {"Skill": "Behavior-Driven Development (BDD)", "Category": "Development Practices"},
    {"Skill": "Refactoring Techniques", "Category": "Development Practices"},
    {"Skill": "Technical Debt Management", "Category": "Development Practices"}
]

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

def extract_skills(text):
    found_skills = []
    for skill in skills_keywords:
        pattern = r"\b" + re.escape(skill["Skill"].lower()) + r"\b"
        if re.search(pattern, text.lower()):
            found_skills.append(skill["Skill"])
    return found_skills

def resume_advisor_view(request):
    score = ""
    suggestions = ""
    user_name = ""
    resume_url = None
    file_path = None

    if request.method == "POST":
        user_name = request.POST.get("Name", "")
        uploaded_file = request.FILES.get('resume')
        if uploaded_file:
            # Save file temporarily
            file_path = default_storage.save(uploaded_file.name, uploaded_file)
            abs_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
            resume_url = settings.MEDIA_URL + file_path

            # === Extract resume text ===
            resume_text = extract_text_from_pdf(abs_file_path)

            # === Load Job Data ===
            csv_path = os.path.join(settings.BASE_DIR, "CSVs", "job_roles.csv")
            job_data = pd.read_csv(csv_path).fillna("")
            job_data['Job_Description'] = job_data['Overview'] + " " + job_data['Key Responsibilities'] + " " + job_data['Required Skills'] + " " + job_data['Tools/Technologies']

            # === Embedding model ===
            model = SentenceTransformer('all-MiniLM-L6-v2')
            job_data['Job_Embedding'] = job_data['Job_Description'].apply(lambda x: model.encode(x, convert_to_tensor=True))
            resume_embedding = model.encode(resume_text, convert_to_tensor=True)

            # === Similarity scoring ===
            similarities = [util.cos_sim(resume_embedding, job_emb)[0].item() for job_emb in job_data['Job_Embedding']]
            job_data['Similarity'] = similarities
            top_match = job_data.sort_values(by='Similarity', ascending=False).iloc[0]

            # === Skill gap analysis ===
            found_skills = extract_skills(resume_text)
            required_skills = [s.strip() for s in top_match['Required Skills'].split(",") if s.strip()]
            missing_skills = [s for s in required_skills if s.lower() not in [fs.lower() for fs in found_skills]]

            score = f"{round(top_match['Similarity'] * 100, 2)}%"
            suggestions = ", ".join(missing_skills)

            # Do NOT delete the file here; keep it for preview

    return render(request, "website/resume_advisor.html", {
        "score": score,
        "suggestions": suggestions,
        "user_name": user_name,
        "resume_url": resume_url
    })

#----------- Newsletter Subscription View -----------

def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Save email if not already subscribed
            if not NewsletterSubscriber.objects.filter(email=email).exists():
                NewsletterSubscriber.objects.create(email=email)
                # Send confirmation email
                send_mail(
                    'CAS Subscription',
                    'You subscribed the CAS notifications',
                    '21b-066-se@students.uit.edu',
                    [email],
                    fail_silently=True,
                )
                messages.success(request, 'Subscribed successfully!')
            else:
                messages.info(request, 'You are already subscribed.')
        else:
            messages.error(request, 'Invalid email address.')
    return redirect('/')