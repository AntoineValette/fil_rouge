def printArticle(article):
    # Paper ID
    paper_id = article.get("paperId") or "N/A"
    print(f"Paper ID          : {paper_id}")

    # External IDs
    external_ids = article.get("externalIds")
    if external_ids:
        ext_ids = ", ".join([f"{k}: {v}" for k, v in external_ids.items()])
    else:
        ext_ids = "N/A"
    print(f"External IDs      : {ext_ids}")

    # Corpus ID
    corpus_id = article.get("corpusId") or "N/A"
    print(f"Corpus ID         : {corpus_id}")

    # Publication Venue
    publication_venue = article.get("publicationVenue")
    if publication_venue:
        venue_name = publication_venue.get("name") or "N/A"

        # Vérifier et formater les alternate_names
        alternate_names = publication_venue.get("alternate_names")
        if alternate_names:
            venue_alternate_names = ", ".join(alternate_names)
        else:
            venue_alternate_names = "N/A"
        # URL de la publication venue
        venue_url = publication_venue.get("url") or "N/A"
        # ISSN de la publication venue
        venue_issn = publication_venue.get("issn") or "N/A"
        # Vérifier et formater les alternate_issns
        alternate_issns = publication_venue.get("alternate_issns")
        if alternate_issns:
            venue_alternate_issns = ", ".join(alternate_issns)
        else:
            venue_alternate_issns = "N/A"
    else:
        venue_name = "N/A"
        venue_alternate_names = "N/A"
        venue_url = "N/A"
        venue_issn = "N/A"
        venue_alternate_issns = "N/A"

    print(f"Publication Venue       : {venue_name}")
    print(f"Alternate Names         : {venue_alternate_names}")
    print(f"URL                     : {venue_url}")
    print(f"ISSN                    : {venue_issn}")
    print(f"Alternate ISSNs         : {venue_alternate_issns}")

    # URL
    url = article.get("url") or "N/A"
    print(f"URL               : {url}")

    # Title
    title = article.get("title") or "N/A"
    print(f"Title             : {title}")

    # Venue (champ 'venue')
    venue = article.get("venue") or "N/A"
    print(f"Venue             : {venue}")

    # Year
    year = article.get("year") or "N/A"
    print(f"Year              : {year}")

    # Fields of Study
    fields = article.get("fieldsOfStudy")
    fields_str = ", ".join(fields) if fields else "N/A"
    print(f"Fields Of Study   : {fields_str}")

    # s2FieldsOfStudy
    s2_fields = article.get("s2FieldsOfStudy")
    if s2_fields:
        s2_fields_str = ", ".join(
            [f"{field.get('category', 'N/A')} ({field.get('source', 'N/A')})" for field in s2_fields]
        )
    else:
        s2_fields_str = "N/A"
    print(f"s2Fields Of Study : {s2_fields_str}")

    # Publication Types
    pub_types = article.get("publicationTypes")
    pub_types_str = ", ".join(pub_types) if pub_types else "N/A"
    print(f"Publication Types : {pub_types_str}")

    # Publication Date
    pub_date = article.get("publicationDate") or "N/A"
    print(f"Publication Date  : {pub_date}")

    # Journal
    journal = article.get("journal")
    if journal:
        journal_name = journal.get("name") or "N/A"
        journal_volume = journal.get("volume") or "N/A"
        journal_pages = journal.get("pages") or "N/A"
        journal_info = f"{journal_name} (Volume: {journal_volume}, Pages: {journal_pages})"
    else:
        journal_info = "N/A"
    print(f"Journal           : {journal_info}")

    # Authors
    authors = article.get("authors")
    if authors:
        authors_str = ", ".join([author.get("name", "N/A") for author in authors])
    else:
        authors_str = "N/A"
    print(f"Authors           : {authors_str}")

    # Abstract
    abstract = article.get("abstract")
    abstract = abstract.strip() if abstract else "N/A"
    print(f"Abstract          : {abstract}")

    # TLDR
    tldr = article.get("tldr")
    tldr = tldr.strip() if tldr else "N/A"
    print(f"tldr              : {tldr}")

    print("-" * 80)