# latexmk para o ufcTex: roda o makeglossaries (lista de siglas e glossário)
# entre as compilações. Uso: latexmk documento.tex
$pdf_mode = 1;
add_cus_dep('acn', 'acr', 0, 'run_makeglossaries');
add_cus_dep('glo', 'gls', 0, 'run_makeglossaries');
$clean_ext .= ' acr acn alg glo gls glg ist lol loq bbl';
sub run_makeglossaries {
  my ($base_name, $path) = fileparse($_[0]);
  # Sem \makeglossaries ativo (glossário comentado), não há o que processar.
  my $aux = "$path$base_name.aux";
  if (open(my $fh, '<', $aux)) {
    my $found = grep { /\\\@istfilename/ } <$fh>;
    close($fh);
    return 0 unless $found;
  }
  pushd $path;
  my $return = system "makeglossaries", $base_name;
  popd;
  return $return;
}
