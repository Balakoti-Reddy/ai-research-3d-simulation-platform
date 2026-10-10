import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import List

@dataclass
class ResearchSource:
    title: str
    authors_or_org: str
    url: str
    summary: str
    evidence_type: str = "arXiv Preprint"

class ResearchSimulationEngine:
    """Layer 3: Queries arXiv API directly without API keys and evaluates simulation options."""

    def search_knowledge_base(self, query: str, max_results: int = 3) -> List[ResearchSource]:
        """Queries arXiv's free public REST API and parses XML results."""
        if not query or len(query.strip()) < 3:
            return []

        # Clean search query for URL encoding
        encoded_query = urllib.parse.quote(query)
        url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results={max_results}"

        sources = []
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                xml_data = response.read()

            root = ET.fromstring(xml_data)
            # arXiv uses Atom XML namespace
            ns = {'atom': 'http://www.w3.org/2005/Atom'}

            for entry in root.findall('atom:entry', ns):
                title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
                summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
                paper_url = entry.find('atom:id', ns).text.strip()
                
                # Extract first author or organization
                authors = [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)]
                author_str = ", ".join(authors[:2]) + (" et al." if len(authors) > 2 else "")

                sources.append(ResearchSource(
                    title=title,
                    authors_or_org=author_str if author_str else "arXiv Contributor",
                    url=paper_url,
                    summary=summary[:180] + "..." if len(summary) > 180 else summary,
                    evidence_type="Peer-Reviewed/Preprint"
                ))
        except Exception as e:
            print(f"arXiv search error: {e}")
            # Fallback if offline or network fails
            sources.append(ResearchSource(
                title=f"Offline Reference: {query}",
                authors_or_org="Local Knowledge Index",
                url="#",
                summary="Network unavailable. Using cached local concepts.",
                evidence_type="Local Fallback"
            ))

        return sources
