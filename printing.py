def print_top_matching_resumes(result_group):
    for job_id, group_data in result_group:
        print("\nJob ID:", job_id)
        print("Cosine Similarity | Domain Resume | Domain Description")
        print(group_data[['similarity', 'domainResume', 'domainDesc']])