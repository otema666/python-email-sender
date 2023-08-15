def truncate_filename(filename, max_length):
    if len(filename) <= max_length:
        return filename
    
    # Calculate the lengths of the first and last parts of the filename
    first_part_length = (max_length - 3) // 2  # Leave space for "..."
    last_part_length = max_length - 3 - first_part_length
    
    # Truncate and add "..." in the middle
    truncated_filename = f"{filename[:first_part_length]}...{filename[-last_part_length:]}"
    return truncated_filename

# Example usage
filename = "very_long_filename_that_needs_truncating.txt"
max_length = 20
truncated_filename = truncate_filename(filename, max_length)
print(truncated_filename)