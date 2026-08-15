use etl_db
go

CREATE TABLE dbo.TABLE_ETL_PIPELINE_RUN_CONTROL (
    -- Unique Identifier for each pipeline run
    RUN_CTRL_ID INT IDENTITY(1,1) NOT NULL,
    
    -- Pipeline Details
    PIPELINE_NAME NVARCHAR(100) NOT NULL,
    RUN_STATUS NVARCHAR(50) NOT NULL, -- e.g., 'Running', 'Completed', 'Failed'
    
    -- Timestamps
    START_TIME DATETIME2 NOT NULL,
    END_TIME DATETIME2 NULL,          -- Updated when the pipeline finishes
    
    -- Metrics (Optional but highly recommended for logging)
    RECORDS_LOADED INT DEFAULT 0,
    ERROR_MESSAGE NVARCHAR(MAX) NULL,  -- Captures Python exceptions if it fails
    
    -- Audit Trail
    CREATED_AT DATETIME2 DEFAULT GETDATE(),
    UPDATED_AT DATETIME2 DEFAULT GETDATE(),
    CREATED_BY NVARCHAR(100) DEFAULT SYSTEM_USER,
    UPDATED_BY NVARCHAR(100) DEFAULT SYSTEM_USER,
    
);