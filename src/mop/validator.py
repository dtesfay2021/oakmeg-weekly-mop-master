from core_funcs import connect_db

def validate_project(proj):
    """
    Validates input against cmp.project to reduce risk of SQL injection.
    
    Raises ValueError if input is not present.
    """
    
    engines = connect_db()
    write_engine = engines[0]
    
    sql = """
        SELECT
            p.program_name
        FROM 
            cmp.program p
        WHERE
            p.id != 0
        ;
        """
    
    with write_engine.connect() as con:
        res = con.execute(sql)
        rows = res.fetchall()
    
    proj_list = [x[0] for x in rows]
    
    if proj not in proj_list:
        print("Project validation: failed")
        raise ValueError(f"'{proj}' is not in the CMP. Please check spelling.")
    
    else:
        print("Project validation: passed")