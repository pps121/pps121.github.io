import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Update Navigation Links
nav_match = re.search(r'<div class="nav-links">(.*?)</div>', content, re.DOTALL)
if nav_match:
    nav_inner = nav_match.group(1)
    # The new order: About, Awards, Papers, Research, Expertise, Experience, Contact
    new_nav = """
      <a href="#about">About</a>
      <a href="#awards">Awards</a>
      <a href="#publications">Papers</a>
      <a href="#research">Research</a>
      <a href="#expertise">Expertise</a>
      <a href="#experience">Experience</a>
      <a href="#contact">Contact</a>
"""
    content = content.replace(nav_match.group(0), f'<div class="nav-links">{new_nav}    </div>')

# 2. Extract Sections
def extract_section(content, section_id):
    # This finds the start of the section and the next <section> or end of body
    pattern = rf'(<section id="{section_id}".*?>.*?(?=</section>\s*<section|</section>\s*<!--|</section>\s*</body>|</section>\s*<footer|</section>\s*$))</section>'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        full_match = match.group(0)
        # Remove it from content so we can place it later
        content = content.replace(full_match, f'<!-- PLACEHOLDER_{section_id} -->')
        return full_match, content
    return None, content

# Extract sections
stats_sec, content = extract_section(content, "stats")
about_sec, content = extract_section(content, "about")
awards_sec, content = extract_section(content, "awards")
publications_sec, content = extract_section(content, "publications")
research_sec, content = extract_section(content, "research")
expertise_sec, content = extract_section(content, "expertise")
experience_sec, content = extract_section(content, "experience")
contact_sec, content = extract_section(content, "contact")

# Remove stats completely by replacing its placeholder with empty string
content = content.replace('<!-- PLACEHOLDER_stats -->', '')

# Remove all other placeholders so we can append them cleanly after hero
for sec_id in ["about", "awards", "publications", "research", "expertise", "experience", "contact"]:
    content = content.replace(f'<!-- PLACEHOLDER_{sec_id} -->', '')

# Construct the new order of sections
ordered_sections = "\n\n".join(filter(None, [
    about_sec,
    awards_sec,
    publications_sec,
    research_sec,
    expertise_sec,
    experience_sec,
    contact_sec
]))

# Place them after hero section
hero_pattern = r'(<section id="hero".*?</section>)'
hero_match = re.search(hero_pattern, content, re.DOTALL)

if hero_match:
    hero_full = hero_match.group(1)
    new_body = hero_full + "\n\n" + ordered_sections
    content = content.replace(hero_full, new_body)

# Write the result back
with open('index.html', 'w') as f:
    f.write(content)

print("Reordering complete.")
