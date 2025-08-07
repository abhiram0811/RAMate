"""
PDF Parser for RAMate - Processes training documents for RA assistance.
Extracts and chunks text from PDF files with metadata preservation.
"""

import os
import json
import re
from typing import List, Dict, Any
from pathlib import Path
import PyPDF2
from dotenv import load_dotenv

load_dotenv()

class PDFProcessor:
    """Handles PDF parsing and text chunking for RAG pipeline."""
    
    def __init__(self, pdf_directory: str, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Initialize PDF processor.
        
        Args:
            pdf_directory: Path to directory containing PDF files
            chunk_size: Target size for text chunks (in characters)
            chunk_overlap: Overlap between consecutive chunks
        """
        self.pdf_directory = Path(pdf_directory)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.documents = []
        
    def extract_text_from_pdf(self, pdf_path: Path) -> List[Dict[str, Any]]:
        """
        Extract text from a PDF file page by page.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of dictionaries containing page text and metadata
        """
        pages = []
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    text = page.extract_text()
                    
                    # Clean up the extracted text
                    text = self._clean_text(text)
                    
                    if text.strip():  # Only add pages with actual content
                        pages.append({
                            'text': text,
                            'page_number': page_num,
                            'source_file': pdf_path.name,
                            'total_pages': len(pdf_reader.pages)
                        })
                        
        except Exception as e:
            print(f"Error processing {pdf_path}: {str(e)}")
            
        return pages
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize extracted text.
        
        Args:
            text: Raw text from PDF
            
        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that might interfere
        text = re.sub(r'[^\w\s\.\,\!\?\:\;\-\(\)\[\]\'\"\/]', '', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def chunk_text(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Split text into overlapping chunks for better retrieval.
        
        Args:
            text: Text to chunk
            metadata: Metadata to attach to each chunk
            
        Returns:
            List of text chunks with metadata
        """
        chunks = []
        
        # Simple word-based chunking
        words = text.split()
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = ' '.join(chunk_words)
            
            if chunk_text.strip():
                chunk_metadata = metadata.copy()
                chunk_metadata.update({
                    'chunk_index': len(chunks),
                    'text': chunk_text,
                    'word_count': len(chunk_words)
                })
                chunks.append(chunk_metadata)
                
        return chunks
    
    def create_document_links(self, filename: str) -> str:
        """
        Create a link to the original document.
        For now, returns a placeholder. In production, this could be:
        - A link to internal document management system
        - A shared drive link
        - A local file path for development
        
        Args:
            filename: Name of the PDF file
            
        Returns:
            Document link URL
        """
        # For development - you can replace this with actual document URLs
        return f"file:///{self.pdf_directory.absolute()}/{filename}"
    
    def process_all_pdfs(self) -> List[Dict[str, Any]]:
        """
        Process all PDF files in the directory.
        
        Returns:
            List of all document chunks with metadata
        """
        all_chunks = []
        
        if not self.pdf_directory.exists():
            raise FileNotFoundError(f"PDF directory not found: {self.pdf_directory}")
        
        pdf_files = list(self.pdf_directory.glob("*.pdf"))
        
        if not pdf_files:
            print(f"No PDF files found in {self.pdf_directory}")
            return []
        
        print(f"Processing {len(pdf_files)} PDF files...")
        
        for pdf_file in pdf_files:
            print(f"Processing: {pdf_file.name}")
            
            # Extract pages from PDF
            pages = self.extract_text_from_pdf(pdf_file)
            
            # Create document link
            doc_link = self.create_document_links(pdf_file.name)
            
            # Process each page
            for page_data in pages:
                # Add document link to metadata
                page_data['document_link'] = doc_link
                page_data['document_title'] = self._format_title(pdf_file.name)
                
                # Chunk the page text
                chunks = self.chunk_text(page_data['text'], page_data)
                all_chunks.extend(chunks)
        
        print(f"Created {len(all_chunks)} total chunks from {len(pdf_files)} documents")
        return all_chunks
    
    def _format_title(self, filename: str) -> str:
        """
        Format filename into a readable document title.
        
        Args:
            filename: PDF filename
            
        Returns:
            Formatted title
        """
        # Remove .pdf extension and replace special characters
        title = filename.replace('.pdf', '')
        title = re.sub(r'[_\-\.]', ' ', title)
        title = ' '.join(word.capitalize() for word in title.split())
        return title
    
    def save_chunks_to_json(self, chunks: List[Dict[str, Any]], output_path: str):
        """
        Save processed chunks to JSON file for inspection/debugging.
        
        Args:
            chunks: List of document chunks
            output_path: Path to save JSON file
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(chunks)} chunks to {output_path}")


def main():
    """Main function to test PDF processing."""
    
    # Load configuration
    pdf_dir = os.getenv('PDF_DIRECTORY', '../pdfs')
    chunk_size = int(os.getenv('CHUNK_SIZE', 500))
    chunk_overlap = int(os.getenv('CHUNK_OVERLAP', 50))
    
    # Initialize processor
    processor = PDFProcessor(
        pdf_directory=pdf_dir,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    try:
        # Process all PDFs
        chunks = processor.process_all_pdfs()
        
        # Save for inspection
        output_path = 'processed_chunks.json'
        processor.save_chunks_to_json(chunks, output_path)
        
        # Print summary
        print(f"\n📊 Processing Summary:")
        print(f"Total chunks: {len(chunks)}")
        
        if chunks:
            sources = set(chunk['source_file'] for chunk in chunks)
            print(f"Source documents: {len(sources)}")
            for source in sorted(sources):
                source_chunks = [c for c in chunks if c['source_file'] == source]
                print(f"  - {source}: {len(source_chunks)} chunks")
        
    except Exception as e:
        print(f"Error processing PDFs: {str(e)}")


if __name__ == "__main__":
    main()
