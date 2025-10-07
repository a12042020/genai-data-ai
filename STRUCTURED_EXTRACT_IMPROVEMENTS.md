# Rich UI Improvements for `structured_extract_baml` Command

## Overview
Enhanced the `structured_extract_baml` CLI command with Rich library for better user experience, progress tracking, and error handling.

## Improvements Made

### 1. **Rich Imports and Setup**
- Added comprehensive Rich imports for progress bars, status indicators, tables, and panels
- Created a global console instance for consistent Rich formatting
- Added time tracking for performance metrics

### 2. **Progress Tracking System**
- **File Discovery**: Status indicator while scanning for markdown files
- **Cache Checking**: Progress indicator when checking existing KV store entries
- **File Reading**: Visual feedback for each file being read with success/error indicators
- **BAML Processing**: Real-time progress bar showing document processing with completion counts
- **Concurrent Processing**: Progress updates for async BAML operations

### 3. **Enhanced Error Handling**
- **Rich Error Display**: Formatted error messages with icons (✓ success, ✗ error, ℹ info)
- **Error Statistics**: Tracking and aggregation of all errors encountered
- **Error Details Table**: Summary table showing up to 10 most recent errors
- **File-specific Errors**: Clear attribution of errors to specific files

### 4. **Statistics Tracking**
- **ProcessingStats Class**: Comprehensive tracking of:
  - Files discovered
  - Files successfully processed
  - Cache hits
  - Error counts and details
  - Processing time and averages
- **Real-time Updates**: Stats updated throughout processing lifecycle

### 5. **Rich Status Messages**
- **Startup Panel**: Beautiful formatted panel showing processing configuration
- **Progress Indicators**: Spinners and status messages for long-running operations
- **Success/Error Icons**: Visual indicators for each operation outcome
- **Color Coding**: Green for success, red for errors, yellow for warnings, blue for info

### 6. **Summary Reports**
- **Processing Summary Table**: Comprehensive final report with:
  - Total files discovered and processed
  - Cache hit statistics
  - Error counts with color coding
  - Total processing time
  - Average time per file
- **Error Details Panel**: Separate table for detailed error information when errors occur

## Key Features

### Visual Improvements
```
┌─ Starting Processing ─┐
│ BAML-based structured extraction
│ Source: ./reviews/
│ Model: ReviewedOpportunity  
│ Recursive: True
│ Force: False
└────────────────────────┘

✓ Found 15 Markdown files to process
✓ Model class 'ReviewedOpportunity' validated

Processing documents ━━━━━━━━━━ 8/10 00:00:12

✓ Processed: doc_001
✓ Processed: doc_002
✗ Failed to process doc_003: Invalid JSON format
```

### Final Summary
```
┌─ Processing Complete ─┐
│     Processing Summary      │
│ ┌─────────────────┬───────┐ │
│ │ Metric          │ Value │ │
│ ├─────────────────┼───────┤ │
│ │ Files Discovered│    15 │ │
│ │ Files Processed │    13 │ │
│ │ Cache Hits      │     3 │ │
│ │ Errors          │     2 │ │
│ │ Total Time      │ 45.2s │ │
│ │ Avg Time/File   │  3.5s │ │
│ └─────────────────┴───────┘ │
└────────────────────────────┘
```

## Usage Examples

### Basic Usage
```bash
uv run cli structured-extract-baml "*.md" --class ReviewedOpportunity --force
```

### Recursive Processing
```bash
uv run cli structured-extract-baml ./reviews/ --recursive --batch-size 10 --class ReviewedOpportunity
```

## Benefits

1. **Better User Experience**: Clear visual feedback throughout processing
2. **Progress Visibility**: Users can see real-time progress and estimated completion
3. **Error Transparency**: Detailed error reporting with context
4. **Performance Insights**: Processing speed and efficiency metrics
5. **Professional Appearance**: Clean, formatted output that's easy to read
6. **Debugging Aid**: Clear error attribution helps with troubleshooting

## Technical Implementation

- **Non-blocking UI**: Progress bars don't interfere with async processing
- **Exception Handling**: Graceful handling of all error types with Rich formatting
- **Memory Efficient**: Statistics tracking doesn't impact processing performance
- **Consistent Styling**: All Rich components use consistent color scheme and formatting