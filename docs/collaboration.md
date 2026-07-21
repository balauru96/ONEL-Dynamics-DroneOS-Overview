# Collaboration Guidelines

This document explains how to work with the ONEL-Dynamics-DroneOS-Overview repository, collaboration expectations, and areas where community input is welcomed.

## Repository Purpose

**ONEL-Dynamics-DroneOS-Overview** is a **public-safe overview and presentation repository**. It is designed for:

- Demonstrating current progress to potential partners and investors
- Discussing architecture and roadmap with technical collaborators
- Preparing for presentations, grants, and business development
- Onboarding new team members to the project vision

**This is not the private development repository.** The main DroneOS-Lab development continues in a private repository with stricter access controls.

## Public-Safe Commitment

**Do not contribute or commit:**

- Private source code or implementation details from DroneOS-Lab
- Backend logic, mission algorithms, or operational intelligence
- Authentication, token handling, or security implementations
- Private `.env` files, credentials, or API keys
- IP addresses, deployment configurations, or internal infrastructure details
- Private logs, reports, or internal communications
- Claims of production readiness without validation

**Do contribute:**

- Documentation and architecture explanations
- Public-safe design discussions and rationale
- Roadmap updates and progress summaries
- Safety and operational considerations
- Testing procedures and validation checklists
- Hardware setup guides and deployment procedures
- Training materials and operational runbooks

## Collaboration Workflow

### Opening Issues and Discussions

1. **Check existing issues** before opening a new one
2. **Use descriptive titles** that clearly state the topic (e.g., "Add Jetson deployment guide")
3. **For questions:** Use Discussions; use Issues for bugs or feature requests
4. **For security concerns:** Contact the maintainers privately; do not open public issues

### Branching and Pull Requests

1. **Create a branch** from `main`:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/your-feature-name
   ```

2. **Make changes** in your branch:
   - Keep commits focused and descriptive
   - Document changes clearly
   - Do not include private information

3. **Push and open a PR**:
   ```bash
   git push origin feature/your-feature-name
   ```
   - Reference any related issues
   - Describe the purpose and scope of changes
   - Ensure documentation is clear and public-safe

4. **Review process**:
   - All PRs require review before merging
   - Reviewers check for: accuracy, public-safety, clarity, and alignment with project vision
   - Address feedback and push updates; do not force-merge

5. **Merge to main**:
   - All checks must pass (linting, documentation format)
   - Maintainer merges when approved
   - Main branch is always deployable and public-safe

### For Flight-Critical Work

If contributing to mission logic, safety, or PX4 integration:

1. **Open an issue** to discuss approach before coding
2. **Include validation plan**: How will this be tested safely?
3. **Prioritize testability**: Separate logic from hardware; test in SITL first
4. **Document assumptions**: What safety properties does this rely on?
5. **Request senior review**: Flight-critical changes require explicit approval

## Areas Welcoming Collaboration

### Documentation

- Deployment guides (Docker, Jetson, PX4 setup)
- Operational checklists and procedures
- Troubleshooting guides
- API endpoint documentation
- Architecture diagrams and explainers

### Hardware Validation

- Jetson Field Box bench testing procedures
- PX4 autopilot compatibility checklist
- Failsafe and RC override validation scripts
- No-props testing protocols
- Sensor integration guides

### User Interface

- Dashboard wireframes and design review
- Mobile operator interface concepts
- Mission planning UI improvements
- Telemetry visualization suggestions

### Testing and Quality

- SITL test scenario library
- Automated test suite design
- Performance benchmarking
- Edge case identification and handling
- Error logging and diagnostics

### Solar Inspection Workflow

- Inspection protocol design
- Report template and format
- Camera payload integration
- Image analysis and annotation tools
- Customer integration points

### Video and Image Pipeline

- Video codec selection and optimization
- Streaming protocol design
- Image extraction and storage
- Real-time compression and transmission
- Edge preprocessing for bandwidth reduction

### AI Vision Research

- Fault detection model training
- Dataset annotation and curation
- Model quantization for edge deployment
- Real-time inference optimization
- Performance benchmarking

### Business and Grant Preparation

- Regulatory compliance research
- Grant application support
- Market analysis and positioning
- Customer discovery interviews
- Partnership exploration

## Communication and Expectations

### Tone and Respect

- Be professional, clear, and respectful in all communications
- Assume good intent; ask for clarification if uncertain
- Provide constructive feedback with suggestions, not criticism
- Respect time zone differences; use asynchronous communication where possible

### Response Times

- **Bug reports**: Response within 48 hours (may not be fixed immediately)
- **Feature requests**: Reviewed within 1 week
- **Questions**: Answered when possible; complex questions may be discussed in meetings
- **PRs**: Reviewed within 3–5 business days (depending on scope)

### Decision Making

- **Documentation and minor updates**: Maintainer review + approval
- **Significant features or changes**: Discussion in issues first; may require design review
- **Flight-critical or safety changes**: Senior review and explicit approval required
- **Roadmap and priority**: Discussed with team; community input welcomed but not binding

## Meeting and Discussion Forums

- **GitHub Discussions**: For general questions, ideas, and open-ended discussions
- **GitHub Issues**: For bugs, feature requests, and task tracking
- **Scheduled syncs**: (If applicable) Regular meetings for synchronous discussion
- **Email/DMs**: For private or sensitive topics

## Licensing and Attribution

- All contributions are understood to be under the project's license (specify: MIT, Apache 2.0, GPL, etc.)
- Attribution for significant contributions will be acknowledged in release notes or CONTRIBUTORS file
- Reuse of external code or libraries must be properly licensed and cited

## If You Have Concerns

1. **Technical questions**: Open a GitHub Discussion or Issue
2. **Safety or security**: Contact maintainers privately
3. **Process or collaboration issues**: Discuss with project lead
4. **Conflicts of interest**: Be transparent; discuss impact and mitigation

## Resources

- **[Current Status](current_status.md)** – What has been validated, what is pending
- **[Architecture Overview](architecture_overview.md)** – System design and layers
- **[Roadmap](roadmap.md)** – Stages and timeline
- **[Safety Notes](safety_notes.md)** – Critical operational and safety requirements

## Code of Conduct (TBD)

(If your organization has a formal Code of Conduct, link or include it here.)

---

**Thank you for your interest in DroneOS and ONEL Dynamics! We look forward to working with you.**

Contact email: ionutonel96@gmail.com
