"""
Demonstrasi debugging skills
"""
import logging
from utils.logger import setup_logger

# Setup logger
logger = setup_logger('debug_demo')

def contoh_bug_division():
    """Fungsi dengan potential bug: division by zero"""
    logger.info("Testing division function...")
    
    numbers = [10, 5, 0, 2]
    results = []
    
    for num in numbers:
        try:
            # Potential bug: division by zero
            result = 100 / num
            results.append(result)
            logger.debug(f"100 / {num} = {result}")
        except ZeroDivisionError as e:
            logger.error(f"Error: {e} - Tidak bisa membagi dengan nol")
            # Fix: skip zero
            continue
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
    
    return results

def contoh_bug_index():
    """Fungsi dengan potential bug: index out of range"""
    logger.info("Testing list indexing...")
    
    data = [1, 2, 3, 4, 5]
    
    try:
        # Potential bug: index out of range
        for i in range(10):
            value = data[i]  # Akan error saat i >= 5
            logger.debug(f"data[{i}] = {value}")
    except IndexError as e:
        logger.error(f"IndexError: {e}")
        # Fix: use proper bounds
        for i in range(min(10, len(data))):
            value = data[i]
            logger.debug(f"Fixed: data[{i}] = {value}")
    
    return data

def contoh_bug_database():
    """Simulasi bug koneksi database"""
    logger.info("Testing database connection...")
    
    try:
        # Simulasi koneksi database gagal
        raise ConnectionError("Database server not responding")
        
    except ConnectionError as e:
        logger.error(f"Database connection failed: {e}")
        logger.info("Trying alternative connection...")
        
        # Simulasi retry logic
        for attempt in range(3):
            logger.info(f"Retry attempt {attempt + 1}")
            # Implement retry logic here
        
        return False
    except Exception as e:
        logger.error(f"Unexpected database error: {e}")
        return False

def main():
    """Main debugging demonstration"""
    print("=" * 50)
    print("DEBUGGING DEMONSTRATION")
    print("=" * 50)
    
    # Test berbagai bug scenarios
    print("\n1. Testing Division Bug:")
    results1 = contoh_bug_division()
    print(f"   Results: {results1}")
    
    print("\n2. Testing Index Bug:")
    results2 = contoh_bug_index()
    print(f"   Results: {results2}")
    
    print("\n3. Testing Database Bug:")
    success = contoh_bug_database()
    print(f"   Success: {success}")
    
    print("\n" + "=" * 50)
    print("DEBUGGING COMPLETE")
    print("=" * 50)
    
    # Check log file
    print("\nLog file created at: logs/app.log")
    print("Check the log for detailed error messages and debugging info.")

if __name__ == "__main__":
    main()