
        const candidates = JSON.parse(document.getElementById('candidate-data').textContent);
        
        function selectCandidate(index) {
            const data = candidates[index];
            if (!data) return;
            
            // 1. Update active card in sidebar
            document.querySelectorAll('.candidate-card').forEach(card => {
                card.classList.remove('active');
            });
            document.getElementById(`candidate-card-${index}`).classList.add('active');
            
            // 2. Update filename and status badge
            document.getElementById('detailFilename').textContent = data.filename;
            
            const statusBadge = document.getElementById('detailStatusBadge');
            statusBadge.className = `badge-status badge-${data.rec_status_class}`;
            statusBadge.textContent = data.rec_headline;
            
            // 3. Update score ring and percentage text
            document.getElementById('detailScoreText').textContent = data.score;
            
            const ringFg = document.getElementById('detailRingFg');
            const circumference = 2 * Math.PI * 50; // 314.16
            const offset = circumference - (circumference * data.score / 100);
            ringFg.style.strokeDashoffset = offset;
            
            // 4. Update recruiter feedback box styling and texts
            const feedbackBox = document.getElementById('detailFeedbackBox');
            feedbackBox.className = `recruiter-feedback-box bg-${data.rec_status_class}`;
            document.getElementById('detailExplanation').textContent = data.rec_explanation;
            document.getElementById('detailRecommendation').textContent = data.rec_recommendation;
            
            // 5. Update skills counts
            document.getElementById('detailMatchedCount').textContent = data.skills_count.matched;
            document.getElementById('detailMissingCount').textContent = data.skills_count.missing;
            
            // 6. Repopulate matched skills pills
            const matchedContainer = document.getElementById('detailMatchedPills');
            matchedContainer.innerHTML = '';
            if (data.matched_skills && data.matched_skills.length > 0) {
                data.matched_skills.forEach(skill => {
                    const pill = document.createElement('span');
                    pill.className = 'skill-pill matched-pill';
                    pill.textContent = skill;
                    matchedContainer.appendChild(pill);
                });
            } else {
                matchedContainer.innerHTML = '<span class="no-skills-msg">No matched skills detected.</span>';
            }
            
            // 7. Repopulate missing skills pills
            const missingContainer = document.getElementById('detailMissingPills');
            missingContainer.innerHTML = '';
            if (data.missing_skills && data.missing_skills.length > 0) {
                data.missing_skills.forEach(skill => {
                    const pill = document.createElement('span');
                    pill.className = 'skill-pill missing-pill';
                    pill.textContent = skill;
                    missingContainer.appendChild(pill);
                });
            } else {
                missingContainer.innerHTML = '<span class="no-skills-msg text-muted">All requirements satisfied!</span>';
            }
            
            // Auto scroll details panel to top on mobile
            if (window.innerWidth <= 900) {
                document.querySelector('.report-panel').scrollIntoView({ behavior: 'smooth' });
            }
        }
