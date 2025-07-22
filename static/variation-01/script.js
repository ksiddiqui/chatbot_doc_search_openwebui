// Multi-Agentic Document Search Landing Page JavaScript

// DOM Elements
const detailsBtn = document.getElementById('detailsBtn');
const techStackBtn = document.getElementById('techStackBtn');
const drawer = document.getElementById('drawer');
const overlay = document.getElementById('overlay');
const closeDrawer = document.getElementById('closeDrawer');
const drawerTitle = document.getElementById('drawerTitle');
const drawerBody = document.getElementById('drawerBody');

// Content Data
const contentData = {
    details: {
        title: 'Project Details',
        content: `
            <div class="drawer-section">
                <h4><i class="fas fa-info-circle"></i>Project Overview</h4>
                <p>The Multi-Agentic Document Search prototype represents a cutting-edge approach to intelligent document retrieval and analysis. This system leverages advanced AI technologies to provide contextual, accurate, and highly relevant search results.</p>
            </div>
            
            <div class="drawer-section">
                <h4><i class="fas fa-target"></i>Key Objectives</h4>
                <ul>
                    <li><i class="fas fa-check"></i>Develop an interactive chatbot within Open WebUI</li>
                    <li><i class="fas fa-check"></i>Implement Contextual RAG pipeline for enhanced accuracy</li>
                    <li><i class="fas fa-check"></i>Integrate multiple AI agents for collaborative processing</li>
                    <li><i class="fas fa-check"></i>Provide real-time document analysis and insights</li>
                    <li><i class="fas fa-check"></i>Enable natural language querying capabilities</li>
                </ul>
            </div>
            
            <div class="drawer-section">
                <h4><i class="fas fa-cogs"></i>Core Features</h4>
                <ul>
                    <li><i class="fas fa-robot"></i>Multi-agent architecture with specialized roles</li>
                    <li><i class="fas fa-brain"></i>Contextual RAG with Anthropic-style processing</li>
                    <li><i class="fas fa-search"></i>Advanced semantic search capabilities</li>
                    <li><i class="fas fa-chart-line"></i>Real-time performance monitoring</li>
                    <li><i class="fas fa-shield-alt"></i>Secure document processing pipeline</li>
                </ul>
            </div>
            
            <div class="drawer-section">
                <h4><i class="fas fa-calendar-alt"></i>Development Timeline</h4>
                <p>This prototype was developed as part of a technical assessment, showcasing expertise in modern AI frameworks and document processing technologies. The project demonstrates proficiency in:</p>
                <ul>
                    <li><i class="fas fa-code"></i>Full-stack development with AI integration</li>
                    <li><i class="fas fa-database"></i>Vector database implementation and optimization</li>
                    <li><i class="fas fa-network-wired"></i>Multi-agent system orchestration</li>
                    <li><i class="fas fa-tools"></i>DevOps and deployment automation</li>
                </ul>
            </div>
        `
    },
    techStack: {
        title: 'Technology Stack',
        content: `
            <div class="drawer-section">
                <h4><i class="fas fa-layer-group"></i>Architecture Overview</h4>
                <p>Our multi-layered architecture combines state-of-the-art AI frameworks with robust data processing capabilities to deliver exceptional performance and scalability.</p>
            </div>
            
            <div class="tech-item">
                <h5><i class="fas fa-file-alt"></i> Document Processing</h5>
                <p>Docling Data Pipeline for intelligent document parsing and content extraction</p>
            </div>
            
            <div class="tech-item">
                <h5><i class="fas fa-database"></i> Storage & Indexing</h5>
                <p>LlamaIndex + PGVector/PostgreSQL for high-performance vector storage and retrieval</p>
            </div>
            
            <div class="tech-item">
                <h5><i class="fas fa-brain"></i> RAG Methodology</h5>
                <p>Contextual RAG with Anthropic-style embedding, LLM integration, and re-ranking models</p>
            </div>
            
            <div class="tech-item">
                <h5><i class="fas fa-server"></i> Model Hosting</h5>
                <p>Locally hosted models via Ollama for enhanced privacy and performance</p>
            </div>
            
            <div class="tech-item">
                <h5><i class="fas fa-users-cog"></i> Agentic Framework</h5>
                <p>Crew.AI for intelligent agent orchestration and collaborative task execution</p>
            </div>
            
            <div class="tech-item">
                <h5><i class="fas fa-edit"></i> Prompt Optimization</h5>
                <p>Arize Phoenix Prompt Playground for advanced prompt engineering and testing</p>
            </div>
            
            <div class="tech-item">
                <h5><i class="fas fa-chart-bar"></i> Evaluation & Monitoring</h5>
                <p>RAGAs for comprehensive LLMOps including tracing, debugging, and performance metrics</p>
            </div>
            
            <div class="tech-item">
                <h5><i class="fas fa-comments"></i> User Interface</h5>
                <p>Open WebUI integration with Arize Phoenix for seamless chatbot interactions</p>
            </div>
            
            <div class="drawer-section">
                <h4><i class="fas fa-rocket"></i>Performance Highlights</h4>
                <ul>
                    <li><i class="fas fa-tachometer-alt"></i>Sub-second query response times</li>
                    <li><i class="fas fa-expand-arrows-alt"></i>Horizontally scalable architecture</li>
                    <li><i class="fas fa-shield-alt"></i>Enterprise-grade security features</li>
                    <li><i class="fas fa-mobile-alt"></i>Responsive cross-platform compatibility</li>
                    <li><i class="fas fa-cloud"></i>Cloud-ready deployment options</li>
                </ul>
            </div>
            
            <div class="drawer-section">
                <h4><i class="fas fa-tools"></i>Development Tools</h4>
                <ul>
                    <li><i class="fas fa-code-branch"></i>Git version control with automated workflows</li>
                    <li><i class="fas fa-bug"></i>Comprehensive testing and debugging suite</li>
                    <li><i class="fas fa-chart-line"></i>Performance monitoring and analytics</li>
                    <li><i class="fas fa-docker"></i>Containerized deployment pipeline</li>
                </ul>
            </div>
        `
    }
};

// Event Listeners
detailsBtn.addEventListener('click', () => openDrawer('details'));
techStackBtn.addEventListener('click', () => openDrawer('techStack'));
closeDrawer.addEventListener('click', closeDrawerFunc);
overlay.addEventListener('click', closeDrawerFunc);

// Keyboard event listener for ESC key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && drawer.classList.contains('open')) {
        closeDrawerFunc();
    }
});

// Functions
function openDrawer(contentType) {
    const content = contentData[contentType];
    
    // Set content
    drawerTitle.textContent = content.title;
    drawerBody.innerHTML = content.content;
    
    // Show drawer and overlay
    drawer.classList.add('open');
    overlay.classList.add('active');
    
    // Prevent body scroll
    document.body.style.overflow = 'hidden';
    
    // Add animation to drawer content
    setTimeout(() => {
        const sections = drawerBody.querySelectorAll('.drawer-section, .tech-item');
        sections.forEach((section, index) => {
            section.style.opacity = '0';
            section.style.transform = 'translateX(20px)';
            section.style.transition = 'all 0.3s ease-out';
            
            setTimeout(() => {
                section.style.opacity = '1';
                section.style.transform = 'translateX(0)';
            }, index * 100);
        });
    }, 100);
}

function closeDrawerFunc() {
    drawer.classList.remove('open');
    overlay.classList.remove('active');
    
    // Restore body scroll
    document.body.style.overflow = 'auto';
}

// Smooth scroll animation for page load
window.addEventListener('load', () => {
    // Add entrance animation to main elements
    const heroSection = document.querySelector('section');
    const cards = document.querySelectorAll('.card');
    const featureCards = document.querySelectorAll('.feature-card');
    
    // Animate hero section
    heroSection.style.opacity = '0';
    heroSection.style.transform = 'translateY(30px)';
    heroSection.style.transition = 'all 0.8s ease-out';
    
    setTimeout(() => {
        heroSection.style.opacity = '1';
        heroSection.style.transform = 'translateY(0)';
    }, 200);
    
    // Animate cards with staggered delay
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'all 0.6s ease-out';
        
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 400 + (index * 150));
    });
    
    // Animate feature cards
    featureCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'all 0.6s ease-out';
        
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 800 + (index * 100));
    });
});

// Add hover effects for interactive elements
document.addEventListener('DOMContentLoaded', () => {
    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('.btn-primary, .btn-secondary');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                transform: scale(0);
                animation: ripple 0.6s ease-out;
                pointer-events: none;
            `;
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // Add CSS for ripple animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(2);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
});
